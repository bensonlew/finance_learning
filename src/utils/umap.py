import scanpy as sc

def umap(data_mat, k):

    # 首先，我们需要对数据进行一些预处理
    sc.pp.normalize_total(data_mat, target_sum=1e4)
    sc.pp.log1p(data_mat)
    sc.pp.highly_variable_genes(data_mat, min_mean=0.0125, max_mean=3, min_disp=0.5)
    data_mat = data_mat[:, data_mat.var.highly_variable]

    # 然后，我们使用 UMAP 进行降维
    sc.pp.scale(data_mat, max_value=10)
    sc.tl.pca(data_mat, svd_solver='arpack')
    sc.external.pp.umap(data_mat)

    # 最后，我们使用 Louvain 算法进行聚类
    sc.tl.louvain(data_mat)

    # 我们可以使用以下代码来可视化结果
    sc.pl.umap(data_mat, color=['louvain'])

    louvain_clusters = data_mat.obs['louvain']

    new_adata = anndata.AnnData(new_data)
    sc.pp.neighbors(new_adata, n_neighbors=10, use_rep='X')

    # Transform new data using the saved UMAP model
    new_adata.obsm['X_umap'] = umap_model.transform(new_adata.X)