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

def dezPrimeirosCategorias(df):
    q1 = """ SELECT * FROM (SELECT *, row_number() over (PARTITION BY categoria ORDER BY relevancia DESC NULLS LAST) AS post_num FROM df) p WHERE post_num < 11 order by categoria, relevancia desc; """
    unique_categorias = df['CATEGORIA'].unique()
    result_df = None
    for categoria in unique_categorias:
        query = df[(df['CATEGORIA'] == categoria) & (df['QTDE_VIAGENS'] > 0)].head(10)
        result_df = pd.concat([result_df, query], ignore_index=True)
    print(result_df)
    result_query = ps.sqldf(q1)[df.columns[:9]]
    print(result_query)
    print(checaSeTodasColunasSaoIguais(result_df, result_query))

dezPrimeirosCategorias(df=df) 



