import numpy as np

class PCA():
    """
    Principal components analysis,PCA,COV,eig,eig vector
    Parameters¶:
        path：数据集的存放路径
        dim : 数据降维后的维度数
    Attribute:
        means_data : 原数据 - 原数据均值化
        m : 数据集的行数
        n ：数据集的列数
        cov_matrix : 协方差矩阵
        eig_vectors : 协方差矩阵的特征向量
        eig_value : 协方差矩阵求得的特征值
        cum_P : 排序后的特征值, 累积百分比计算
    Method:
        PCA.dataset():数据集导入, return：means_data,array(m,n)
        PCA.cov_matrix:协方差矩阵计算, retrn:cov_matrix,array(n,n)
        PCA.eig_vector:特征值和特征向量计算, return:(eig_value, eig_vectors),(array(1xn),array(n,n))
        PCA.pc:降维后的数据集计算, return:data_rescaled,array(m,dim), defaut:dim=2
    """
    def __init__(self):
        self.means_data = np.array([])  #Max of var data
        self.m = 0        #Data's rows
        self.n = 0        #Data's columns or The number of variables
        self.cov_matrix = np.array([])   #Covariance matrix
        self.eig_vectors = np.array([])  #Eigenvector
        self.eig_value = np.array([])    #Eigenvalues
        self.cum_P = []
        
    def dataset(self,path):
        # Calculate the mean, then Variance maximization
        self.path = path
        self.test_data = np.loadtxt(self.path,delimiter = ',')  #Training data
        means = self.test_data.mean(axis = 0)
        self.m, self.n = self.test_data.shape
        
        for i in range(self.m):
            self.means_data = self.test_data - means
            
        return self.means_data
         
    def COV(self):
        self.cov_matrix = np.cov(self.means_data.T)
        return self.cov_matrix
        
    def eig_vector(self):
        eig_values, eig_vectors = np.linalg.eig(self.cov_matrix)
        self.eig_value = eig_values
        self.eig_vectors = eig_vectors
        return self.eig_value, self.eig_vectors
    
    def pc(self,dim = 2):
        '''defaute 2-dim,you can re-definition'''
        self.dim = dim
        values = self.eig_value  #4x1
        try:
            indices = values.argsort()[::-1] #sort by desc,return index
            evecs = self.eig_vectors[:,indices] #array sort by desc
            evals = self.eig_value[indices]  #1-dim array sort by desc
            p1 = 0  # Cumulative proportion
            for element in evals:
                p1 = element/np.sum(self.eig_value) + p1
                self.cum_P.append(p1)                
                
            evecess = evecs[:, :self.dim] #dim = 2, retuen 4x2 array
            data_rescaled = np.dot(self.test_data,evecess) # dot of a(15x4) and b(4x2)
        except Exception as e:
            print "There raise error:,%s ." % e
        return data_rescaled,self.cum_P  #return new down_dim data
        
'''Test program'''        
if __name__ == "__main__":
    p = PCA()
    #~ print u"均值化后的数据集为：",p.dataset('H:\\PCA_test.txt')
    #~ print u"协方差矩阵为：",p.COV()
    #~ print u"特征向量为：",p.eig_vector()[1]
    #~ print u"新的维度数据集",p.pc(dim=3)[1]