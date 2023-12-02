from numpy.random._examples.cffi.extending import rng
from pandas import DataFrame

from scipy.stats import ortho_group

from evaTour.datasets.datasetFoursquare import readDatasetNYC
from evaTour.datasets.datasetFoursquare import transformDataset
from evaTour.datasets.datasetFoursquare import readDatasetTKY

from scipy.sparse.linalg import svds

import numpy as np
import os


def test01():
    print("test01")

    ratingsNYcDF, itemsNYcDF, distancesNYcDF = readDatasetNYC()
    #ratingsTkyDF, itemsTkyDF, distancesTkyDF = readDatasetTKY()

    print(ratingsNYcDF.head(10))

    numberOfUsers = len(list(set(ratingsNYcDF['UserID'])))
    maxUserID = max(ratingsNYcDF['UserID'])

    print("max: " + str(maxUserID))
    print("numberOfUsers: " + str(numberOfUsers))
    #5/0
    userIDs:int = maxUserID +1
    venueIDs:int = 5109+1
    zeors_array = np.zeros((userIDs, venueIDs))

    for indexI, rowI in ratingsNYcDF.iterrows():
        #print(rowI)
        userID = rowI['UserID']
        venueID = rowI['VenueID']
        #print("userID: " + str(userID))
        #print("venueID: " + str(venueID))
        sizeI = rowI['size']
        zeors_array[userID, venueID] = sizeI

    print("Training started")
    u4, s4, vT4 = svds(zeors_array, k=8)
    print("Training stopped")

    A4 = u4 @ np.diag(s4) @ vT4
    print(A4.shape)
    print(A4[1])

    #all_user_predicted_ratings = np.dot(np.dot(u4, s4), vT4)
    #preds_df = pd.DataFrame(all_user_predicted_ratings, columns = user_item.columns, index=user_item.index)


def test02():
    print("test02")

    orthogonal = ortho_group.rvs(10, random_state=rng)
    s = [1e-3, 1, 2, 3, 4]  # non-zero singular values
    u = orthogonal[:, :5]         # left singular vectors
    vT = orthogonal[:, 5:].T      # right singular vectors
    A = u @ np.diag(s) @ vT
    print(A)

    u4, s4, vT4 = svds(A, k=4)
    print(u4)
    print(s4)
    print(vT4)
    #U, sigma, Vt = svds(ratingsDF, k = 50)


if __name__ == "__main__":
    os.chdir('../../../')
    print("")
    test01()