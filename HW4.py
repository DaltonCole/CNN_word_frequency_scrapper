from surprise import SVD
from surprise import NMF
from surprise import KNNBasic
from surprise import Dataset
from surprise import evaluate, print_perf
from surprise import Reader
import os
import random

random.seed(0)

#load data from a file
file_path = os.path.expanduser('restaurant_ratings.txt')
reader = Reader(line_format='user item rating timestamp', sep='\t')
data = Dataset.load_from_file(file_path, reader=reader)
data.split(n_folds=3)

print("Questions: 9, 10, 11")
print("############################################ SVD ############################################")
algo = SVD()
perf = evaluate(algo, data, measures=['RMSE', 'MAE'])
print_perf(perf)
print()

print("############################################ PMF ############################################")
algo = SVD(biased=False) #PMF
perf = evaluate(algo, data, measures=['RMSE', 'MAE'])
print_perf(perf)
print()

print("############################################ NMF ############################################")
algo = NMF()
perf = evaluate(algo, data, measures=['RMSE', 'MAE'])
print_perf(perf)
print()

print("############################# User based Collaborative Filtering #############################")
algo = KNNBasic(sim_options = {'user_based': True})
perf = evaluate(algo, data, measures=['RMSE', 'MAE'])
print_perf(perf)
print()

print("############################# Item based Collaborative Filtering #############################")
algo = KNNBasic(sim_options = {'user_based': False})
perf = evaluate(algo, data, measures=['RMSE', 'MAE'])
print_perf(perf)
print()

print("Question: 13")
print("############################ User based Collaborative Filtering MSD ###########################")
algo = KNNBasic(sim_options = {'name':'MSD','user_based': True})
perf = evaluate(algo, data, measures=['RMSE', 'MAE'])
print_perf(perf)
print()

print("########################## User based Collaborative Filtering Cosine ##########################")
algo = KNNBasic(sim_options = {'name':'cosine','user_based': True})
perf = evaluate(algo, data, measures=['RMSE', 'MAE'])
print_perf(perf)
print()

print("########################## User based Collaborative Filtering Pearson #########################")
algo = KNNBasic(sim_options = {'name':'pearson','user_based': True})
perf = evaluate(algo, data, measures=['RMSE', 'MAE'])
print_perf(perf)
print()

print("############################ Item based Collaborative Filtering MSD ###########################")
algo = KNNBasic(sim_options = {'name':'MSD','user_based': False})
perf = evaluate(algo, data, measures=['RMSE', 'MAE'])
print_perf(perf)
print()

print("########################## Item based Collaborative Filtering Cosine ##########################")
algo = KNNBasic(sim_options = {'name':'cosine','user_based': False})
perf = evaluate(algo, data, measures=['RMSE', 'MAE'])
print_perf(perf)
print()

print("########################## Item based Collaborative Filtering Pearson #########################")
algo = KNNBasic(sim_options = {'name':'pearson','user_based': False})
perf = evaluate(algo, data, measures=['RMSE', 'MAE'])
print_perf(perf)
print()

print("Question: 14")
for i in range(1,101):
	print(i)
	print("######################### User based Collaborative Filtering MSD K =",i, "##########################")
	algo = KNNBasic(k=i, sim_options = {'name':'MSD','user_based': True})
	perf = evaluate(algo, data, measures=['RMSE', 'MAE'])
	print_perf(perf)
	print()

	print("######################### Item based Collaborative Filtering MSD K =",i, "##########################")
	algo = KNNBasic(k=i, sim_options = {'name':'MSD','user_based': False})
	perf = evaluate(algo, data, measures=['RMSE', 'MAE'])
	print_perf(perf)
	print()

print("Cosine version of Q14")
for i in range(1,101):
	print(i)
	print("######################### User based Collaborative Filtering MSD K =",i, "##########################")
	algo = KNNBasic(k=i, sim_options = {'name':'Cosine','user_based': True})
	perf = evaluate(algo, data, measures=['RMSE'])
	print_perf(perf)
	print()

	print("######################### Item based Collaborative Filtering MSD K =",i, "##########################")
	algo = KNNBasic(k=i, sim_options = {'name':'Cosine','user_based': False})
	perf = evaluate(algo, data, measures=['RMSE'])
	print_perf(perf)
	print()

