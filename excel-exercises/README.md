# Excel Advanced Exercises

## Exercise 1 — IF Formula (Beetle lengths)
- C4 formula: `=IF(B4>$B$21,"LONG","SHORT")`
- D4 formula: `=IF(B4>$B$21,"This sample is "&TEXT(B4-$B$21,"0.00")&" longer than average","")`
- Changed B4 to 50.2 → average increased → many beetles changed to SHORT
- Changed B4 to 20.7 → confirmed D4 shows blank (SHORT beetle)

## Exercise 2 — Holiday Pivot Table
- Created PivotTable from holidays data
- Filtered: Travel Method = Plane, Resort Name starts with S
- Values: Average Price
- Drilled down on Grand Total → confirmed 3 holidays
- Saved file to work folder

## Exercise 3 — Oscar Nominations Pivot Chart
- Created PivotTable: Certificate in Rows, Genre in Columns
- Values: Average Oscar Nominations
- Inserted Column PivotChart
- Added Genre Slicer for dynamic filtering

## Exercise 4 (Optional) — House Search Pivot Table
- Created Calculated Field: Total Rooms = Bedrooms + Bathrooms + Receptions
- Grouped locations: Urban (Town, Village) vs Non-Urban (Countryside, Remote)
- Showed garden size as % of column total by location group

## Exercise 5 (Optional) — Film Slicer
- Replaced Country filter with Country Slicer
- Filtered to Australia and New Zealand
- Created second PivotTable on new sheet: Average Oscar Wins by Certificate
- Connected original slicer to both PivotTables
- Saved as Filming over.xlsx
