# Troop51Mulch
Code to help create routes for Troop51's annual mulch sale


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
4. Add the analysis section at the bottom using a previous year's YEARroutes.ods spreadsheet.  Modify all the formulas to account for different number of orders from year to year.
5. Column L will hold the order number.  Put orders which are physically close together on the same order.  Use the analysis section at the bottom to show how many bags are in the order you are currently working on.  The goal is to hit 320 +/- 5 bags for every order.  Each 26' truck holds 7 pallets and each pallet holds 45 bags, and extra bags on a truck is preferred (except for the first route for each truck - those are already loaded).  Protip: use the split screen to have the analysis section at the bottom always visible while assigning deliveries to routes.  That makes it easy to track how many bags the current route has.
6. Work step 5 from the outliers into the center of mass for all the deliveries.  Kinda spiral in from the outside to the center as you assign routes.  This makes for some ugly routes which can be done early in the day when traffic is lighter.
7. Use http://routexl.com to create "shortest drive times" and "estimated drive times".  Use the import button to copy/paste all the addresses for a single route and paste in the church.  Once the addresses are all imported, set the church as the start AND end and let it generate the drive times.  You'll have to modify slightly - put yourself in the mindset of someone who's running the routes and think about how you'd like to do them.  I tend to make sure as many deliveries happen off the right side of the truck and minimize back tracking (that is, deliver off the left and right side as the truck progresses down the street).  Minimize turns when possible.  Record drive times on the "routes" page of the spreadsheet
8. Estimate total route time by adding drive time and x bags per minute delivery.  Historically 6.0 has been a good number, but I think 5.75 will be better next year, especially if we share that with the drivers.  Three of 5 drivers beat that in 2016.  
9. Assign routes to trucks by estimating who the best drivers will be and giving them the longer routes (not all the longest - that will piss them off and they won't come back next year).  But bias it towards the stronger drivers getting the less easy routes.  Inevitably there will be a route you'll have to chop up at the end of the day to get everyone done as close to the same time as possible, but you can minimize it.

=== This second step works on the output of the manual route preparation ===
1. Export the routes page to a csv file.  Tab delimited, no text delimiters.  Clean up the csv file so only routes are in the file
2. Second step generates the route html pages.  You have to adjust the comments at the bottom of the files.
mkdir routes
./step2.py 2016routes.csv

=== Generate artifacts for delivery day ===
1. Use your browser to print all the html files as pdf
2. Use ghost script to combine them into one big pdf for easy printing `ghostscript -dBATCH -dNOPAUSE -q -sDEVICE=pdfwrite -sOutputFile=finished.pdf rout*`
3. Print two copies of each route.  Copy 1 will be split out for each driver/navigator.  Copy 2 is backup for the yard.
4. Print large master sheet on 11x17 or legal size paper
5. Print a Truck Progress sheet so you can track which route a truck is doing and when you can expect them back
6. in 2016, I gave a copy of the Truck Progress sheet to all the drivers - they actually filled them all out!
