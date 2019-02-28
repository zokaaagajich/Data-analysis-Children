#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report, confusion_matrix
import pandas as pd
import numpy as np
from sys import exit, argv

def main():

    args = argv
    if len(args) != 2:
        exit(f"Usage: {args[0]} path_to_csv_file")

    df = pd.read_csv(args[1])

    #izbacujemo neke nevazne atribute
    df = df.drop(['ID', 'Name', 'Age Group', 'Incident Date', 'Geolocation', 'Gun Types', 'Guns Stolen'], axis=1)
    #izbacujemo instance sa nedostajucim vrednostima
    df = df.replace("N/A", np.nan)
    df = df.dropna()
    #prikaz pocetnih podataka
    print(df.head())

    final_attr = 'Status'
    #izbacujemo Status, njega pogadjamo
    X = df.drop([final_attr], axis=1)
    #ciljni atribut je Status
    y = df[[final_attr]]

    #prikaz
    print("\nX:\n", X.head())
    print("\ny:\n", y.head())

    #sve menjamo jedinstvenim brojevima
    status = df[final_attr].unique()
    status_dict = dict(zip(status, range(len(status))))
    y = y.replace(status_dict)
    #invertovan recnik za status
    inv_dict = {v: k for k, v in status_dict.items()}

    gender = df['Gender'].unique()
    Gender_dict = dict(zip(gender, range(len(gender))))
    X = X.replace(Gender_dict)

    Type = df['Type'].unique()
    Type_dict = dict(zip(Type, range(len(Type))))
    X = X.replace(Type_dict)

    City = df['City'].unique()
    City_dict = dict(zip(City, range(len(City))))
    X = X.replace(City_dict)

    State = df['State'].unique()
    State_dict = dict(zip(State, range(len(State))))
    X = X.replace(State_dict)

    #podela na trening (70%) i test (30%)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3)

    #algoritam k suseda
    knn = KNeighborsClassifier(n_neighbors = 15, weights = 'distance')
    knn.fit(X_train, y_train.values.ravel())

    y_train_predicted = knn.predict(X_train)
    y_test_predicted = knn.predict(X_test)

    #Score
    #report
    report_train = classification_report(y_train, y_train_predicted)
    report_test = classification_report(y_test, y_test_predicted)
    print("report_train:\n", report_train)
    print("report_test:\n", report_test)
    #Matrica konfuzije
    conf_train = confusion_matrix(y_train, y_train_predicted)
    conf_test = confusion_matrix(y_test, y_test_predicted)
    print("confusion matrix train:\n", conf_train)
    print("confusion matrix test:\n", conf_test)


    #pogadjanje ciljnog atributa
    in_data = []
    describe = X.describe()
    print("\nUnesi sledece podatke:")

    for col in describe.columns:
        print('{:20} min: {:6}, max: {:6}'.format(col, describe[col]['min'], describe[col]['max']))
    print()

    try:
        in_state = State_dict[input()]
        in_city = City_dict[input()]
        in_guns = int(input())
        in_type = Type_dict[input()]
        in_age =  int(input())
        in_gender = Gender_dict[input()]
    except KeyError as e:
        print("Dati podatak nije validan!")
        exit(1)

    in_data = [in_state, in_city, in_guns, in_type, in_age, in_gender]
    person = np.array(in_data)
    person = person.reshape(1, -1)
    print("Uneta osoba je: ", inv_dict[knn.predict(person)[0]])


if __name__ == "__main__":
    main()
