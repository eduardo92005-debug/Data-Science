import pandas as pd
import pandasql as ps

df = pd.read_json('../database.json')


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

def dezPrimeirosCidadesSemRepetirCategoria(df):
    #exportarParaExcel(new_df)
    df = df[(df['QTDE_VIAGENS'] > 0) & (df['QTD_PONTOS'] > 100)]
    unique_cidades = df['CIDADE'].unique()
    unique_categorias = df['CATEGORIA'].unique()
    df = df.sort_values(by=['CATEGORIA', 'RELEVANCIA'], ascending=[True, False])
    df_ranking_cidade_by_categoria = None
    for cidade in unique_cidades:
        df_fixed = df[(df['CIDADE'] == cidade)]
        for categoria in unique_categorias:
            newdf = df_fixed[df_fixed['CATEGORIA'] == categoria]
            the_largest_relevancia = newdf.head(1)
            df_ranking_cidade_by_categoria = pd.concat([df_ranking_cidade_by_categoria,the_largest_relevancia])
    df_ranking_cidade_by_categoria = df_ranking_cidade_by_categoria.sort_values(by=['CIDADE', 'RELEVANCIA'], ascending=[True, False])
    result_df = None
    for cidade in unique_cidades:
        query = df_ranking_cidade_by_categoria[df_ranking_cidade_by_categoria['CIDADE'] == cidade]
        the_ten_largest = query.head(10)
        result_df = pd.concat([result_df,the_ten_largest])
    result_df = result_df.sort_values(by=['CIDADE', 'RELEVANCIA'], ascending=[True, False])
    print(result_df)
    q1 = """
SELECT * FROM
(    
     SELECT * FROM    
(    
 SELECT *,
    DENSE_RANK () OVER ( 
        PARTITION BY cidade
        ORDER BY relevancia desc
    ) post_num2
 FROM   
 (    
        SELECT *,
        DENSE_RANK () OVER ( 
        PARTITION BY categoria, cidade
        ORDER BY relevancia desc
    ) post_num
        FROM (SELECT *, avg(relevancia) as relevancia
    FROM df
    where qtde_viagens > 0 and qtd_pontos >100
    group by categoria, estado, cidade) as tb
) tb2
  where post_num=1
)   
  where post_num2<11
    
) tb3
    order by cidade, relevancia desc
    """
    result_query = ps.sqldf(q1)[df.columns[:9]]
    print("######## RESULTADO SQL #############")
    print(result_query)
    exportarParaExcel(result_query,'sql.xlsx')
    print(checaSeTodasColunasSaoIguais(result_df, result_query))


dezPrimeirosCidadesSemRepetirCategoria(df=df)


