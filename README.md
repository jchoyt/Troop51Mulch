http://tinyurl.com/troop51mulch goes to http://soulcubes.com/medcafe/index.html

= How to prep the spreadsheet =
1. Open in LibreOffice Calc or Microsoft Excel
2. Delete all rows from the last order to the end
3. Delete the first row
4. (optional, but good practice) Delete all columns after column S
5. Fill out junk content in all rows in column S - this is discarded by the code, but is needed to make easy parsing of the rows possible.  I just copy the # down.
6. Delete any pure donation rows (where there's no address).  You'll have to copy and "paste special" over all the order numbers to paste in the values, not the formulas
7. Save as CSV file with Tab delimiter and no text delimiter.  Check for non-ASCII characters (slanted ' seem to be popular).  If you have a text editor that you can specify the character set in, set it to US-ASCII and it'll hunt down all the weird characters for you

= Running the first stage python script =
Need to import pygmaps:
export PYTHONPATH=/home/jchoyt/devel/boyscouts/pygmaps-0.1.1

processOrders has two stages.  First stage checks and caches all addresses:
./step1.py Mulch_Sale_2015.csv

= Manual route preparation =
1. After all orders are in, redirect the step 1 output to a csv file:  `./step1.py Mulch_Sale_2016.csv > 2016routes.csv`
2. Clean up any extraneous output at the top of the file.   All that should be there is a set of tab-delimted tuples
3. Open in LibreCalc or Excel and make sure it cleanly separated the columns.  Columns should be order no, last name, first name, phone number, neighborhood, street address, city, state, zip, comments, number of bags
4. Add the analysis seciton at the bottom using a previous year's YEARroutes.ods spreadsheet.  Modify all the formulas to account for different number of orders from year to year.
5. Column L will hold the order number.  Put orders which are physically close together on the same order.  Use the analysis section at the bottom to show how many bags are in the order you are currently working on.  The goal is to hit 320 +/- 5 bags for every order.  Each 26' truck holds 7 pallets and each pallet holds 45 bags, and extra bags on a truck is preferred (except for the first route for each truck - those are already loaded).  Protip: use the split screen to have the analysis section at the bottom always visible while assigning deliveries to routes.  That makes it easy to track how many bags the current route has.
6.


=== This second step works on the output of the first ===
Second step generates the route html pages.  You have to adjust the comments at the bottom of the files.
mkdir routes
./step2.py 2015routes.csv



=== Generate artifacts for delivery day ===
1. Use your browser to print all the html files as pdf
2. Use ghost script to combine them into one big pdf for easy printing `ghostscript -dBATCH -dNOPAUSE -q -sDEVICE=pdfwrite -sOutputFile=finished.pdf rout*`
3. Print two copies of each route.  Copy 1 will be split out for each driver/navigator.  Copy 2 is backup for the yard.
4. Print large master sheet on 11x17 or legal size paper
5. Print Truck Progress sheet so you can track which route a truck is doing and when you can expect them back

<!-- :wrap=soft:noTabs=true:mode=markdown: -->
