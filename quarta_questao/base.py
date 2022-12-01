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

def rodoviariaCadaCidade(df):
    unique_cidades = df['CIDADE'].unique()
    result_df = None
    for cidade in unique_cidades:
        query = df[(df['CIDADE'] == cidade) & (df['CATEGORIA'] == 'Rodoviárias') & (df['QTDE_VIAGENS'] > 1000)].head(1)
        result_df = pd.concat([result_df, query])
    print("######## RESULTADO PANDAS #############")
    print(result_df)
    q1 = """
    SELECT * FROM    
(  
        SELECT *,
        DENSE_RANK () OVER ( 
        PARTITION BY categoria, cidade
        ORDER BY relevancia desc
    ) post_num
        FROM
    (SELECT *, avg(relevancia) as relevancia
    FROM df
    where qtde_viagens > 1000
    group by pto_turistico, categoria, cidade) as tb
) tb2
  where post_num=1 and categoria = 'Rodoviárias'
  order by relevancia desc, cidade
    """
    result_query = ps.sqldf(q1)[df.columns[:9]]
    print("######## RESULTADO SQL #############")
    print(result_query)
    print(checaSeTodasColunasSaoIguais(result_df, result_query))


rodoviariaCadaCidade(df=df) 



