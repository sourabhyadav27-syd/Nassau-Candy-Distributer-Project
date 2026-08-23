CREATE DATABASE Projects;
USE Projects;

SELECT * FROM PR_Dataset;

SELECT count(`Gross Margin %`)
FROM PR_Dataset;

DESCRIBE PR_Dataset;

=======================================================================================================================================================
                                         ----------------- BASIC EDA ---------------------
=======================================================================================================================================================


SELECT 
round(SUM(`Sales`),2) AS Total_Sales,
round(SUM(`Gross Profit`),2) AS Total_Gross_Profit,
round(SUM(`Cost`),2) AS Total_Cost
FROM PR_Dataset;

SELECT 
round(
AVG(`Gross Margin %`),2)
 as AVG_Gross_Margin
FROM PR_Dataset;

======================================================================================================================================================
                                             ----- PRODUCT-LEVEL PROFITABILITY ANALYSIS ----
=======================================================================================================================================================


----------------------- PRODUCT RANK BY PROFIT -----------------------

SELECT `Product Name`,sum(`Gross PRofit`) AS Total_Gross_Profit, 
RANK()
OVER (ORDER BY sum(`Gross Profit`) DESC) AS Product_Rank
FROM PR_Dataset
GROUP BY `Product Name`;

----------------------- PRODUCT RANK BY MARGIN ------------------

SELECT `Product Name`,avg(`Gross Margin %`) AS Total_Gross_Margin,
RANK() 
OVER(order by avg(`Gross Margin %`) DESC) AS Product_Rank
FROM PR_Dataset
GROUP BY `Product Name`; 

-------------------- HIGH-PROFIT / HIGH-MARGIN PRODUCTS --------------

SELECT
    `Product Name`,
    ROUND(SUM(Sales),2) AS Sales,
    ROUND(SUM(`Gross Profit`),2) AS Gross_Profit,
    ROUND((SUM(`Gross Profit`)/SUM(Sales))*100,2) AS Gross_Margin
FROM PR_Dataset
GROUP BY `Product Name`
HAVING Gross_Margin >= 60
ORDER BY Gross_Profit DESC;

-------------------- HIGH-SALES / LOW-MARGIN PRODUCTS ----------------

SELECT
    `Product Name`,
    ROUND(SUM(Sales),2) AS Sales,
    ROUND(SUM(`Gross Profit`),2) AS Gross_Profit,
    ROUND((SUM(`Gross Profit`)/SUM(Sales))*100,2) AS Gross_Margin
FROM PR_Dataset
GROUP BY `Product Name`
HAVING Gross_Margin < 60
ORDER BY Sales DESC;

-------------------- LOW-SALES / LOW-PROFIT PRODUCTS -----------------

SELECT
    `Product Name`,
    ROUND(SUM(Sales),2) AS Sales,
    ROUND(SUM(`Gross Profit`),2) AS Gross_Profit
FROM PR_Dataset
GROUP BY `Product Name`
ORDER BY Sales ASC, Gross_Profit ASC
LIMIT 5;


=======================================================================================================================================================
                                         ----- DIVISION-LEVEL PERFORMANCE ANALYSIS --------
=======================================================================================================================================================                                         
                                         

----------------- AGGREGATE METRICS BY DIVISION -----------------

SELECT
    Division,
    ROUND(SUM(Sales),2) AS Total_Sales,
    ROUND(SUM(Cost),2) AS Total_Cost,
    ROUND(SUM(`Gross Profit`),2) AS Total_Gross_Profit,
    ROUND((SUM(`Gross Profit`) / SUM(Sales)) * 100,2) AS Gross_Margin
FROM PR_Dataset
GROUP BY Division
ORDER BY Total_Gross_Profit DESC;

-------------- COMPARE: AVERAGE MARGIN BY DIVISION ------------

SELECT
    Division,
    ROUND(AVG(CAST(REPLACE(`Gross Margin %`,'%','') AS DECIMAL(10,2))),2) AS Avg_Margin
FROM PR_Dataset
GROUP BY Division
ORDER BY Avg_Margin DESC;

-------------------- COMPARE: REVENUE VS PROFIT IMBALANCE ---------------

SELECT
    Division,
    ROUND(SUM(Sales),2) AS Revenue,
    ROUND(SUM(`Gross Profit`),2) AS Profit
FROM PR_Dataset
GROUP BY Division
ORDER BY Revenue DESC;

--------------------  DIVISION WITH STRONG FINANCIAL EFFICIENCY --------------

SELECT
    Division,
    ROUND(SUM(Sales),2) AS Sales,
    ROUND(SUM(`Gross Profit`),2) AS Profit,
    ROUND((SUM(`Gross Profit`) / SUM(Sales)) * 100,2) AS Margin
FROM PR_Dataset
GROUP BY Division
HAVING Margin >= 65
ORDER BY Margin DESC;

-------------------- DIVISION WITH STRUCTURAL MARGIN ISSUES -------------

SELECT
    Division,
    ROUND(SUM(Sales),2) AS Sales,
    ROUND(SUM(`Gross Profit`),2) AS Profit,
    ROUND((SUM(`Gross Profit`) / SUM(Sales)) * 100,2) AS Margin
FROM PR_Dataset
GROUP BY Division
HAVING Margin < 60
ORDER BY Margin;


=======================================================================================================================================================
                                      -------- PROFIT CONCENTRATION (PARETO) ANALYSIS ------
=======================================================================================================================================================                                      
                                      

SELECT `Product Name`,
ROUND(SUM(Sales),2) AS Total_Sales,
ROUND(SUM(`Gross Profit`),2) AS Total_Profit
FROM PR_Dataset
GROUP BY `Product Name`
ORDER BY Total_Sales , Total_Profit DESC;

----------- PRODUCT-WISE REVENUE CONTRIBUTION % -----------

   SELECT `Product Name`,
    ROUND(SUM(Sales),2) AS Total_Sales,
    ROUND(SUM(Sales) * 100 /SUM(SUM(Sales)) OVER (),2) AS Revenue_Contribution_Percentage
FROM PR_Dataset
GROUP BY `Product Name`
ORDER BY Total_Sales DESC;

-----------------  PARETO QUERY (80% REVENUE) --------------SELECT


SELECT
    `Product Name`,
    ROUND(SUM(Sales),2) AS Total_Sales,
    ROUND(SUM(Sales) * 100 /SUM(SUM(Sales)) OVER (),2) AS Revenue_Contribution,
	ROUND(SUM(SUM(Sales)) 
    OVER(ORDER BY SUM(Sales) DESC) * 100 /SUM(SUM(Sales)) OVER(),2) AS Cumulative_Revenue
FROM PR_Dataset
GROUP BY `Product Name`
ORDER BY Total_Sales DESC;


-----------------------  PARETO QUERY (80% PROFIT) -------------


SELECT
    `Product Name`,
    ROUND(SUM(`Gross Profit`),2) AS Total_Gross_Profit,
    ROUND(SUM(`Gross Profit`) * 100 /SUM(SUM(`Gross Profit`)) OVER (),2) AS Gross_Profit_Contribution,
    ROUND(SUM(SUM(`Gross Profit`)) OVER(ORDER BY SUM(`Gross Profit`) DESC) * 100 /SUM(SUM(`Gross Profit`)) OVER(),2) AS Cumulative_Gross_Profit
FROM PR_Dataset
GROUP BY `Product Name`
ORDER BY Total_Gross_Profit DESC;


=======================================================================================================================================================
					                  ----------------- COST STRUCTURE DIAGNOSTICS --------------
=======================================================================================================================================================                        
 
----------------------- COST VS SALES SCATTER ANALYSIS ------------------------

SELECT `Product Name`,
ROUND(SUM(Sales),2) AS Total_Sales,
ROUND(SUM(Cost),2) AS Total_Cost
FROM PR_Dataset
GROUP BY `Product Name`
ORDER BY Total_Cost DESC;

----------------------- COSTLY AND POOR-MARGIN PRODUCTS ----------------

SELECT
    `Product Name`,
    ROUND(SUM(Sales),2) AS Total_Sales,
    ROUND(SUM(Cost),2) AS Total_Cost,
    ROUND(SUM(`Gross Profit`),2) AS Total_Profit,
    ROUND(AVG(`Gross Margin %`),2) AS AVG_Gross_Margin
FROM PR_Dataset
GROUP BY `Product Name`
ORDER BY AVG_Gross_Margin ASC,Total_Cost DESC;

-------------------- PRICE INEFFICENCY OF PRODUCTS --------------------

SELECT
    `Product Name`,
    ROUND(SUM(Sales),2) AS Total_Sales,
    ROUND(SUM(Cost),2) AS Total_Cost,
    ROUND(AVG(`Gross Margin %`),2) AS Avg_Gross_Margin,
    CASE
        WHEN AVG(`Gross Margin %`) < 50 THEN 'Pricing Inefficiency'
        ELSE 'Healthy Pricing'
    END AS Status
FROM PR_Dataset
GROUP BY `Product Name`
ORDER BY Avg_Gross_Margin ASC;

-------------------- PRODUCT NEEDING REPRICING  -------------

SELECT
    `Product Name`,
    ROUND(AVG(`Gross Margin %`),2) AS Avg_Gross_Margin,
    CASE
        WHEN AVG(`Gross Margin %`) < 50 THEN 'Needs Repricing'
        ELSE 'Pricing is Good'
    END AS Pricing_Status
FROM PR_Dataset
GROUP BY `Product Name`
ORDER BY Avg_Gross_Margin ASC;

-------------------- COST RENEGOTIATION -------------------

SELECT
    `Product Name`,
    ROUND(SUM(Sales),2) AS Total_Sales,
    ROUND(SUM(Cost),2) AS Total_Cost,
    ROUND(SUM(`Gross Profit`),2) AS Total_Gross_Profit,
    CASE
        WHEN SUM(Cost) >= SUM(`Gross Profit`)
        THEN 'Renegotiate Cost'
        ELSE 'Cost Acceptable'
    END AS Recommendation
FROM PR_Dataset
GROUP BY `Product Name`
ORDER BY Total_Cost DESC;

-------------------- DISCONTINUATION REVIEW ----------------

SELECT
    `Product Name`,
    ROUND(SUM(Sales),2) AS Total_Sales,
    ROUND(SUM(`Gross Profit`),2) AS Total_Gross_Profit,
    CASE
        WHEN SUM(Sales) < 5000
         AND SUM(`Gross Profit`) < 1000
        THEN 'Discontinuation Review'

        ELSE 'Continue'
    END AS Recommendation
FROM PR_Dataset
GROUP BY `Product Name`
ORDER BY Total_Sales ASC, Total_Gross_Profit ASC;




