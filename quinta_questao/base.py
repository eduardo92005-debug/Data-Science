import pandas as pd
import pandasql as ps

df = pd.read_json('../database.json')
df = df.sort_values(by=['CATEGORIA', 'RELEVANCIA'], ascending=[True, False])


def exportarParaExcel(df, path=r'excel.xlsx'):
    df.to_excel(path,'default', index=False)
#exportarParaExcel(df,'excel2.xlsx')
def printaUmaColuna(df1,col):
    print(df1[df1.columns[col]])

def diferencaSimetricaEntreTabelas(df1,df2,col):
    return set(sorted(df1[df1.columns[col]])).symmetric_difference(set(sorted(df2[df2.columns[col]])))


def checaSeTodasColunasSaoIguais(df1,df2):
    qntd_colunas = df.shape[1] - 1
    contador_igualdade = 0
    for i in range(0,qntd_colunas):
        df1_s = sorted(df1[df1.columns[i]])
        df2_s = sorted(df2[df2.columns[i]])
        if(df1_s == df2_s):
            contador_igualdade += 1
        else:
            return i
    return contador_igualdade == qntd_colunas

def dezPrimeirosEstadosSemRepetirCategoria(df):
    unique_estados = df['ESTADO'].unique()
    unique_categorias = df['CATEGORIA'].unique()
    df = df[df['QTDE_VIAGENS'] > 0]
    result_df = None
    for estado in unique_estados:
        for categoria in unique_categorias:
            query = df[(df['ESTADO'] == estado) & (df['CATEGORIA'] == categoria)].head(1)
            result_df = pd.concat([result_df, query])
    result_df = result_df.sort_values(by=['ESTADO','RELEVANCIA'], ascending=[True, False])
    new_df = None
    for estado in unique_estados:
        query = result_df[(result_df['ESTADO'] == estado)].head(10)
        new_df = pd.concat([new_df, query])
    new_df = new_df.sort_values(by=['ESTADO','RELEVANCIA'], ascending=[True, False])
    print("######## RESULTADO PANDAS #############")
    print(new_df)
    #exportarParaExcel(new_df)
    q1 = """
    SELECT * FROM
(    
     SELECT * FROM    
(    
 SELECT *,
    DENSE_RANK () OVER ( 
        PARTITION BY estado
        ORDER BY relevancia desc
    ) post_num2
 FROM   
 (    
        SELECT *,
        DENSE_RANK () OVER ( 
        PARTITION BY categoria, estado
        ORDER BY relevancia desc
    ) post_num
        FROM
    (SELECT *, avg(relevancia) as relevancia
    FROM df
    where qtde_viagens > 0
group by pto_turistico, categoria, estado) as tb
) tb2
  where post_num=1
)   
  where post_num2<=10
    
) tb3
    order by estado, relevancia desc
    """
    result_query = ps.sqldf(q1)[df.columns[:9]]
    print("######## RESULTADO SQL #############")
    print(result_query)
    #exportarParaExcel(result_query,'sql.xlsx')
    print(checaSeTodasColunasSaoIguais(new_df, result_query))


dezPrimeirosEstadosSemRepetirCategoria(df=df) 


