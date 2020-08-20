#Data Preporcessing
df_cluster['date_diff'] = pd.to_datetime("now").date() - df['Shop Created At'].dt.date
df_cluster['date_diff'] = df_cluster['date_diff'].apply(lambda x: float(x.days))

one_hot = pd.get_dummies(df_cluster["Shop Commerce Background"])
# Drop column as it is now encoded
df_cluster = df_cluster.drop("Shop Commerce Background",axis = 1)
# Join the encoded df
df_cluster = df_cluster.join(one_hot)

# Normalize total_bedrooms column
x_array = np.array(df_cluster["Total_shop_gmv"])
normalized_X = preprocessing.normalize([x_array])
one_hot_mrr = pd.get_dummies(df_cluster["Current MRR Band Range"])
shop_dim_gmv_pd = df_cluster.drop("Current MRR Band Range",axis = 1)
shop_dim_gmv_pd = shop_dim_gmv_pd.join(one_hot_mrr)

df_trunc = df_cluster[['Total_shop_gmv_normalized','Total_shop_transactions', 'date_diff', 'aspirational', 'experimental', 'intentional', 'unknown','$0.00',
                                 '$0.01-$20.00',
                            '$1000.01-$1900.00',
                              '$150.01-$350.00',
                                    '$1900.01+',
                                '$20.01-$50.00',
                             '$350.01-$1000.00',
                               '$50.01-$150.00',
         'Not Yet Known Current MRR Band Range',
               'Unknown Current MRR Band Range']]
gmm = GMM(n_components=4).fit(df_trunc)
labels = gmm.predict(df_trunc)
probs = gmm.predict_proba(df_trunc)
