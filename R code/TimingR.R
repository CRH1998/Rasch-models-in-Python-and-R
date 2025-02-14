library(eRm)          # Rasch model

library(dplyr)        # Data manipulation
library(data.table)   # Data manipulation
library(reshape)      # Data manipulation

library(readr)        # Data import

library(ggplot2)      # Data visualization
library(RASCHplot)    # Data visualization

source("C:/Users/brf337/Desktop/Rasch package/R code/SimulateRaschData.R") # Source simulation function


# Timing different simulations

bench::mark(SML_sim(k = 10, n = 150),
            SML_sim(k = 10, n = 200),
            SML_sim(k = 10, n = 250),
            SML_sim(k = 10, n = 500),
            SML_sim(k = 10, n = 1000),
            SML_sim(k = 20, n = 150),
            SML_sim(k = 20, n = 200),
            SML_sim(k = 20, n = 250),
            SML_sim(k = 20, n = 500),
            SML_sim(k = 20, n = 1000),
            SML_sim(k = 50, n = 150),
            SML_sim(k = 50, n = 200),
            SML_sim(k = 50, n = 250),
            SML_sim(k = 50, n = 500),
            SML_sim(k = 50, n = 1000),
            SML_sim(k = 100, n = 150),
            SML_sim(k = 100, n = 200),
            SML_sim(k = 100, n = 250),
            SML_sim(k = 100, n = 500),
            SML_sim(k = 100, n = 1000),
            iterations = 100,
            check = FALSE)


################################################################################
#                                Timing RM()                                   #
################################################################################


SML_sim10150 <- SML_sim(k = 10, n = 150)
SML_sim10200 <- SML_sim(k = 10, n = 200)
SML_sim10250 <- SML_sim(k = 10, n = 250)
SML_sim10500 <- SML_sim(k = 10, n = 500)
SML_sim20150 <- SML_sim(k = 20, n = 150)
SML_sim20200 <- SML_sim(k = 20, n = 200)
SML_sim20250 <- SML_sim(k = 20, n = 250)
SML_sim20500 <- SML_sim(k = 20, n = 500)

SML_sim101000 <- SML_sim(k = 10, n = 1000)
SML_sim201000 <- SML_sim(k = 20, n = 1000)


bench::mark(RM(SML_sim201000, sum0 = TRUE), iterations = 5,
            check = FALSE)


























################################################################################
#                             LEGACY CODE                                      #
################################################################################


t0_1000x10 <- Sys.time()
SML.test_sim1000x10 <- SML_sim(k = 10, n = 1000)
t1_1000x10 <- Sys.time()
t1_1000x10 - t0_1000x10


t0_1000x100 <- Sys.time()
SML.test_sim1000x100 <- SML_sim(k = 100, n = 1000)
t1_1000x100 <- Sys.time()
t1_1000x100 - t0_1000x100


t0_1000x150 <- Sys.time()
SML.test_sim1000x150 <- SML_sim(k = 150, n = 1000)
t1_1000x150 <- Sys.time()
t1_1000x150 - t0_1000x150


t0_10000x10 <- Sys.time()
SML.test_sim10000x10 <- SML_sim(k = 10, n = 10000)
t1_10000x10 <- Sys.time()
t1_10000x10 - t0_10000x10


t0_10000x100 <- Sys.time()
SML.test_sim10000x100 <- SML_sim(k = 100, n = 10000)
t1_10000x100 <- Sys.time()
t1_10000x100 - t0_10000x100






# Timing different models
t0_1000x10 <- Sys.time()
SML.fit1000x10 <- RM(SML.test_sim1000x10, sum0 = TRUE)
t1_1000x10 <- Sys.time()
t1_1000x10 - t0_1000x10


t0_10000x10 <- Sys.time()
SML.fit10000x10 <- RM(SML.test_sim10000x10, sum0 = TRUE)
t1_10000x10 <- Sys.time()
t1_10000x10 - t0_10000x10



t0_1000x100 <- Sys.time()
SML.fit1000x100 <- RM(SML.test_sim1000x100, sum0 = TRUE)
t1_1000x100 <- Sys.time()
t1_1000x100 - t0_1000x100


t0_1000x150 <- Sys.time()
SML.fit1000x150 <- RM(SML.test_sim1000x150, sum0 = TRUE)
t1_1000x150 <- Sys.time()
t1_1000x150 - t0_1000x150


t0_10000x100 <- Sys.time()
SML.fit10000x100 <- RM(SML.test_sim10000x100, sum0 = TRUE)
t1_10000x100 <- Sys.time()
t1_10000x100 - t0_10000x100

