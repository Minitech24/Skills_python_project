# Data Analytics Tool ## Introduction#This program is intended to complete a full data analyis.#It is able to pre-process the data set and give descriptive analysis results, all based on the users preferences.#The focus lies on being interactive and automated. In other words, the program contains specifically designed function for which it asks the user desires to perform these on her data set.#Any kind of csv file should be applicable. The user needs make sure the csv file is located in the correct directory.## 1. Import of libraries and the data set # 1.1 Importsimport sysimport mathimport numpy as npimport pandas as pdimport scipy.statsimport matplotlib.pyplot as pltplt.style.use('ggplot')import seaborn as snprint("Hello User!\nLet's begin analysing your data!")# 1.2 preparing answers for y/n questions and colums list needed for yes = {"yes", "y"}no = {"no", "n"}cancel = {"cancel", "c"}# 1.3 define function for reading data def start():    inp = input("\nIs your csv file located in the correct working directory?(y/n): ")    if inp in yes:        global data        data = pd.read_csv("listings.csv")        print("In the following tables you get an overview of your data including the head and tail:")        return    elif start in no:        print("\nPlease put your csv file in the correct working directory!")        start()    else:         sys.stdout.write("""\nPlease answer with "yes" or "no".""")        start()# 1.3 cont. Execute functionstart()data.head()data.tail()# 1.4 more preparationcolumns = list(data.columns) c = []d = []## 1.5 showing max rows and columns of data setprint("\nYour data set includes the following number of rows and columns: ")data.shape## 2. Cleaning Data Set## 2.1 defining an input function such that we can run this everytime the program needs to ask the user for columns ## the user may like to editdef getInput():    global c    c.clear()    input_string = input("\nEnter all columns separated with space: ")    c  = input_string.split(" ")    if input_string in cancel:        return    for char in c:         if char not in columns:            print(char, "is not given in data set. Please retry!")            getInput()    return ## 2.2 removing columns# define function that asks for columns and deletes them def qRemove():    inp = str(input("\nWould you like to remove columns from your data set? (y/n): ").lower())    if inp in yes:        getInput()        global data        data = data.drop(c, axis = 1) # axis = 1 --> column        for char in c:            print("\n" + char, "has been removed from the data set!")        return     elif inp in no:        return    else:        sys.stdout.write"""\nPlease answer with "yes" or "no".""")        qRemove()    return## 2.2 cont. Execute functionqRemove()## 2.3 get further details of the data types print("""In the next table you will find more specific information about your data set:("datetime64" stands for date data, int64" and "float64" stands for numeric data,\nwhereas "object" denotes categorical data)\n""")data.dtypes## 2.4 Transforming data types# here we want to ask the user if there are columns present that the user wants to change the type in# for this we create define functions for each column type and insert these into our main function #define category change functiondef inpCat():    inp =str(input("\nAre there columns that need to be changed into character type? (y/n): ").lower())    if inp in yes:        getInput()        for char in c:            global data            data[char] = data[char].astype(str)            print(char, "has been changed to character!")        return    elif inp in no:        return    else:         sys.stdout.write("""\nPlease answer with "yes" or "no".""")        inpCat()        # define float change functiondef inpNum():    inp = str(input("\nAre there columns that need to be changed into numeric? (y/n): ").lower())    if inp in yes:        getInput()        for char in c:            global data            data[char] = pd.to_numeric(data[char])            print(char, "has been changed to numeric!")        return    elif inp in no:        return    else:         sys.stdout.write("""\nPlease answer with "yes" or "no".""")        inpNum()      #define date change functiondef inpDate():    inp = str(input("\nAre there columns that need to be changed into date? (y/n): ").lower())    if inp in yes:        getInput()        for char in c:            try:                dateFormat =str(input("\nFor " + str(char) + ", please enter the correct format of the date (eg. %Y-%m-%d): "))                global data                data[char] = pd.to_datetime(data[char], format=dateFormat)                print(char, "has been changed to date!")            except ValueError:                print("Time data does not match format", dateFormat +". Insert correct format!\nTry again!")                inpDate()        return    elif inp in no:        return    else:         sys.stdout.write("""\nPlease answer with "yes" or "no".""")        inpDate()    # define main Transform functiondef qTransform():    inp = str(input("\nAre there any columns in the wrong format that need to be changed? (y/n): ?").lower())    if inp in yes:        inpCat()        inpNum()        inpDate()        return    elif inp in no:        return    else:        sys.stdout.write("""\nPlease answer with "yes" or "no".""")        qTransform()    return# 2.4 cont. Execute functionqTransform()print("\nSee the table with your prefered types:")data.dtypes## 2.5 count number of null valuesprint("Here you see the number of null values for each variable.")data.isnull().sum()## 2.6 remove NA values# define function to ask if user wants to remove null valuesdef qDrop():    inp = str(input("\nDo you want to remove the null values? (y/n): ").lower())    if inp in yes:        global data        data = data.dropna(how="any", axis=0) # axis = 0 --> row        print("\nNull values have been removed!")    elif inp in no:        return          else:        sys.stdout.write("""\nPlease answer with "yes" or "no".""")        qDrop()# 2.6 cont. Execute function        qDrop()## 2.7 Renaming columns # define function to ask if user wants to rename columnsdef qRename():    inp = str(input("\nDo you want to rename columns? (y/n): ").lower())    if inp in yes:        getInput()        for char in c:            global data            newname_input = str(input("\nHow do you want to rename the column " + str(char) + "?: "))            data = data.rename(columns = {char: newname_input})            print(str(char) +" has been renamed to " + str(newname_input)+"!")    elif inp in no:        return          else:        sys.stdout.write("""\nPlease answer with "yes" or "no".""")        qRename()## 2.7 cont. Execute functionqRename()## 2.8 check for duplicates # To get rid of duplicates we check if the *key* appears more than once# A key in a data set is a variable which is unique. In other words, the key is the value whith which# you can access each single observation. # Thus the program asks the user for the key. The user must know this key! # The program hasn't got the intelligence to figure it out by itself. # defining question for keydef Key():    key = input("\nWhat column is the primary key of your data set?: ")    if key in cancel:        return    elif key not in columns:        print("\nThere is no such column. Please try again!")        qKey()    else:        return key# defining removal of duplicates def removeDupl():    inp = str(input("\nDo you want to remove the duplicates from your data set? (y/n): ").lower())    if inp in yes:        global data        data = data.drop_duplicates(key)        print("\nThe duplicates have been removed!")    elif inp in no:        return     else:        sys.stdout.write("""\nPlease answer with "yes" or "no".""")        removeDupl()    return#defining overall question for handling duplicatesdef qDuplicates():    inp = str(input("\nDo you want to check for duplicates in your data set? (y/n): ").lower())    if inp in yes:        global key        key = Key()        duplications = sum(data.duplicated(key))        print("There are", duplications, "duplicates in your data set.")        if duplications == 0:            return        else:            removeDupl()    elif inp in no:         return    else:        sys.stdout.write("""\nPlease answer with "yes" or "no".""")        qDuplicates()      return# 2.8 cont. Execute functionsqDuplicates()## 2.9 asking if everything is correct and give user the possibility to repeat correctionsdef qAgainNested():    again = str(input("What would you like to repeat? Enter the corresponding letter (a-e): ").lower())            if again == "cancel":        q2Again()        return    elif again == "a":        qRemove()        q2Again()    elif again == "b":        qTransform()        q2Again()    elif again == "c":        qDrop()        q2Again()    elif again == "d":        qRename()        q2Again()    elif again == "e":        qDuplicates()        q2Again()    else:         sys.stdout.write("""\nPlease answer with a letter between "(a-e)".""")        qAgainNested()def q2Again():    inp2 = str(input("\nDo you want to repeat another function? (y/n): ").lower())    if inp2 in yes:        qAgain()    elif inp2 in no:        print("\nPerfect!\nWe are left with the following number of observations and variables:\n" +               str(data.shape[0]) + " | " + str(data.shape[1]))    else:        sys.stdout.write("""\nPlease answer with "yes" or "no".""")        q2Again()  def qAgain():    inp = str(input("\nDo you want to repeat one of these listed functions?"+                    "\na) Removing Columns" +                     "\nb) Transforming data types"+                    "\nc) remove NA values"+                    "\nd) Renaming columns"+                    "\ne) Check for duplicates"+                    "\n (y/n): ")).lower()    if inp in yes:        qAgainNested()    elif inp in no:        print("\nPerfect!\nWe are left with the following number of observations and variables:\n" +               str(data.shape[0]) + " | " + str(data.shape[1]))    else:        sys.stdout.write("""\nPlease answer with "yes" or "no".""")        qAgain()        ## 2.9 cont. Exectute functionsqAgain()## 3. Univariate Analysisdef getCat():    global d    d.clear()    input_string = input("\nEnter all key related character type columns: ")    d  = input_string.split(" ")    if d in cancel:        return##  3.0.1 split numerical and categorical data into two listsprint("\nWe now continue with our analyis of the data."+     "\nFor the next step please enter all key related character type columns and" +      " other character type columns in the next field that you think have *subgroups > 80*!" +     "\nOtherwise the results for plotting may become unsatisfying and even lead to errors.")# define function to separate numerical and categorical data into two listsdef qVariableType():        # numerical variables    num_variables = data.select_dtypes(include=["int64","float64"]).columns    # categorical variables    cat_variables = data.select_dtypes(include=["object"]).columns    getCat()    try:        cat_variables = cat_variables.drop(d)    except KeyError:        print("You have entered a non categorical column. Please retry!")        qVariableType()    return list(num_variables), list(cat_variables)# 3.0.1 cont. Execute functionnum_variables, cat_variables = get_variable_type()print("\nYour data has been split into two categories:\nNumerical and Categorical"+      "\nYour data set contains", str(len(num_variables)), "numerical and", str(len(cat_variables)), "categorical variables.")## 3.1 Categorical Data analysis# 3.1.1 grid plotting categorical data# it takes all categorical variables and plots them into a histogram# it is sometimes messy for some variables with large number of subgroups . print("\nBelow you can explore a grid of count plots including all the categorical data of your data set:\n")cat_melt = pd.melt(data, value_vars=sorted(cat_variables))cat_grid = sn.FacetGrid(cat_melt, col="variable", col_wrap=4, sharex=False, sharey=False)plt.xticks(rotation="vertical")cat_grid = cat_grid.map(sn.countplot, "value", color = "lightcoral",)[plt.setp(ax.get_xticklabels(), rotation=90) for ax in cat_grid.axes.flat]plt.show()### Specific categorical analysis# Here the program starts with looking at a categorical values individually. The user chooses which and how many columns he wants to inspect.def getSingleInput():    global e    inp = str(input("Enter a single variable: "))    e = inp    if e in cancel:        return    elif e not in d:        print(e, "is not given in the list for categorical columns. Please retry!")        getSingleInput()getSingleInput()## 3.1.2 value_counts #counts the number of each single group of category and presents result in a small dfdef qCat():    inp = str(input("\nDo you want to look at a specific categorical column individually? (y/n): ")).lower()    if inp in yes:        getInput()        countCat()    elif inp in no:        return    else:        sys.stdout.write("""\nPlease answer with "yes" or "no".""")        qCat()    def countCat():    for char in c:        a = data[char].value_counts()        return a    returncountCat()## 3.1.3 ask for repetitiondef AgainCat():    inp = str(input("Do you want to do the same analyis for another categorical variable? (y/n): ")).lower()    if inp in yes:        qCat()        AgainCat()    elif inp in no:         print("\nWe now move on to the numerical values.")    else:         sys.stdout.write("""\nPlease answer with "yes" or "no".""")        AgainCat()## 3.1.3 cont. Execute functionAgainCat()## 3.2 Numerical Data analysis## 3.2.1 distribution grid plot of all numerical variables# takes all numerical variables and plots them into an distribution plotprint("\nBelow you can explore a grid of distribution plots including all the numerical data of your data set:\n")num_melt = pd.melt(data, value_vars=sorted(num_variables))num_grid = sn.FacetGrid(num_melt, col="variable", col_wrap=4, sharex=False, sharey=False)num_grid = num_grid.map(sn.distplot, "value", color = "lightcoral")###  Specific Numeric analysisLike before for categorical data the program here asks which *numerical* columns the user wants to inspect more specifically.## 3.2.2 define function to ask which variables the user wants to inspect individuallydef qNumValue():    inp = str(input("\nDo you want to examine any numerical columns individually? (y/n): ").lower())    if inp in yes:        getInput()    elif inp in no:        return    else:        sys.stdout.write("""\nPlease answer with "yes" or "no".""")        qNumValue()## 3.2.2 cont. Execute functionqNumValue()## 3.2.3 define function for a descriptive summarydef Summary():    for char in c:        mean = data[char].mean()        median = data[char].median()        std = data[char].std()        mini = data[char].min()        q_25 = data[char].quantile(q=0.25)        q_50 = data[char].quantile(q=0.5)        q_75 = data[char].quantile(q=0.75)        maxi = data[char].max()        print("\nVariable " +str(char)+ " possesses the following properties:\n\nmean: \t\t", round(mean, 2),              "\nmedian: \t", round(median, 2),             "\nstd: \t\t", round(std, 2),             "\nmin: \t\t", round(mini, 2),             "\n25%: \t\t", round(q_25, 2),             "\n50%: \t\t", round(q_50, 2),             "\n75%: \t\t", round(q_75, 2),             "\nmax: \t\t", round(maxi, 2))     return  ## 3.2.3 cont. Execute functionSummary()## 3.2.4 define function for inspecting Skew & Kurtosisdef SkewKurtosis():    for char in c:        skew = data[char].skew()        kurtosis = data[char].kurtosis()        print("\nResults for " + str(char) + ":")        print("Skew: ", round(skew, 2) , "| Kurtosis: ", round(kurtosis, 2))        if skew >= -0.5 and skew <= 0.5:            print("\nA skew value of", round(skew,2), "indicates a fairly symmetric distribution.")        elif skew > 0.5 and skew <=1:            print("\nA skew value of", round(skew,2), "indicates a moderately right skewed distribution.")        elif skew >1:            if skew > 10:                print("\nA skew value of", round(skew,2), "indicates an extremely right skewed distribution.")            else:                print("\nA skew value of", round(skew,2), "indicates a highly right skewed distribution.")        elif skew >= -1 and skew <-0.5:            print("\nA skew value of", round(skew,2), "indicates a moderately left skewed distribution.")        elif skew <-1:              if skew <-10:                print("\nA skew value of", round(skew,2), "indicates an extremely left skewed distribution.")            else:                print("\nA skew value of", round(skew,2), "indicates a highly left skewed distribution.")        if kurtosis <2.9:            if kurtosis<0:                print("The kurtosis with a value of", round(kurtosis,2), "may indicate a bimodal distribution with two different modes.")            if kurtosis >= 0:                print("The kurtosis with a value of", round(kurtosis,2), "is platykurtic.\nThis indicates a low and broad peak.\nIn addition, this means that the distribution is shorter and tails are thinner.\nOutliers are less likely")        elif kurtosis >3.1:             if kurtosis > 30:                print("The kurtosis with a value of", round(kurtosis,2), "is extremely leptokurtic.\nThis indicates a very high and sharp peak.\nIn addition, this means that the distribution is long and fat tails are observable.\nOutliers are highly possible.")            else:                print("The kurtosis with a value of", round(kurtosis,2), "is leptokurtic.\nThis indicates a high and sharp peak.\nIn addition, this means that the distribution is long and fat tails are observable.\nOutliers are highly possible.")        elif kurtosis >=2.9 and kurtosis <= 3.1:            print("The kurtosis with a value of", round(kurtosis,2), "is Mesokurtic.\nThis indicates a similar distribution to a normal distribution.")    return                   ## 3.2.4 cont. Execute functionSkewKurtosis()## 3.2.5 count outliersdef Outliers():    for char in c:        q_25 = data[char].quantile(q=0.25)        q_75 = data[char].quantile(q=0.75)        print("\nThe total number of outliers for " + str(char) + " is", sum((data[char]<q_25) | (data[char]>q_75)), ".")    return                ## 3.2.5 cont. Execute functionOutliers()## 3.2.6 plotting boxplot to further # price should equal chosen variabledef Boxplot():    for char in c:        print("\nBelow you can examine a boxplot based on the variable " + str(char)+":")        plt.figure(figsize=(14,4))        data[char].plot.box(vert = False)        plt.show()    return## 3.2.6 cont. Execute functionBoxplot()## 3.2.7 ask if user wants to repeat numerical analysis for other variablesdef AgainNum():    inp = str(input("Do you want to do the same analyis for another numeric variables? (y/n): ")).lower()    if inp in yes:        qNumValue()        Summary()        SkewKurtosis()        Outliers()        Boxplot()        AgainNum()    elif inp in no:         print("\nWe now move on to our correlation matrix.")    else:         sys.stdout.write("""\nPlease answer with "yes" or "no".""")        AgainNum()## 3.2.7 cont. Execute functionAgainNum()## 3.2.8 correlation Matrix of the numerical variablesprint("\nLastly, you can see a correlation matrix based on the numeric variables." +      "\nPlease inspect it for potential and interesting correlations in your data set!")sn.set(style="white")corr = data.corr()fig = plt.figure(figsize=(14,12))ax = fig.add_subplot(111)cmap = sn.diverging_palette(220, 10, as_cmap=True)mask = np.triu(np.ones_like(corr, dtype=np.bool))sn.heatmap(corr,            xticklabels=corr.columns.values,           yticklabels=corr.index.values,           mask=mask,           cmap="RdPu")ax.xaxis.tick_bottom()plt.setp(ax.get_xticklabels(), rotation=60)plt.show()print("You have finished the data analyis!")