import csv
import json
from collections import defaultdict

def cleanPass2():
	with open("cleaned2.csv", "w", newline="") as outfile:

		header = """Census year,Block ID,Property ID,Base property ID,Building name,Street address,CLUE small area,Construction year,Refurbished year,Number of floors (above ground),Predominant space use,Accessibility type,Accessibility type description,Accessibility rating,Bicycle spaces,Has showers,Longitude,Latitude,Location"""
		sHeader = header.split(",")

		sHeader = [
			"Census year",
			"Block ID",
			"Property ID",
			"Base property ID",
			"CLUE small area",
			"Construction year",
			"Refurbished year",
			"Number of floors (above ground)",
			"Predominant space use",
			"Latitude",
			"Longitude",
		]
						
		colMap = {
			"Census year": sHeader.index("Census year"),
			"Block ID": sHeader.index("Block ID"),
			"Property ID": sHeader.index("Property ID"),
			"Base property ID": sHeader.index("Base property ID"),
			"CLUE small area": sHeader.index("CLUE small area"),
			"Construction year": sHeader.index("Construction year"),
			"Refurbished year": sHeader.index("Refurbished year"),
			"Number of floors (above ground)": sHeader.index("Number of floors (above ground)"),
			"Predominant space use": sHeader.index("Predominant space use"),
			"Latitude": sHeader.index("Latitude"),
			"Longitude": sHeader.index("Longitude"),
		}

		output = csv.writer(outfile)
		output.writerow(colMap.keys())

		yearColumn = list(colMap.keys()).index("Census year")
		clueAreaColumn = list(colMap.keys()).index("CLUE small area")
		floorsColumn = list(colMap.keys()).index("Number of floors (above ground)")
		usageColumn = list(colMap.keys()).index("Predominant space use")
		blockIdColumn = list(colMap.keys()).index("Block ID")

		collatedCLUE = defaultdict(int)
		collatedCLUE2 = defaultdict(lambda: defaultdict(int))
		collatedCLUE2Floors = defaultdict(lambda: defaultdict(float))
		collatedCLUE3 = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
		collatedCLUE3Floors = defaultdict(lambda: defaultdict(lambda: defaultdict(float)))

		collatedCLUE4 = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(int))))
		collatedCLUE4MaxFloors = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(int))))
		collatedCLUE4Floors = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(float))))

		with open("cleaned.csv") as csvfile:
			spamreader = csv.reader(csvfile)
			i = 0
			for row in spamreader:
				#skip header
				if i < 1:
					i += 1
					continue
				resRow = []

				for col in colMap.keys():
					resRow.append(row[colMap[col]])

				if(resRow[floorsColumn] != ''):
					collatedCLUE[(resRow[yearColumn], resRow[clueAreaColumn])] += 1

					collatedCLUE2[resRow[clueAreaColumn]][resRow[yearColumn]] += 1
					collatedCLUE2Floors[resRow[clueAreaColumn]][resRow[yearColumn]] += int(resRow[floorsColumn])
					collatedCLUE3[resRow[clueAreaColumn]][resRow[usageColumn]][resRow[yearColumn]] += 1
					collatedCLUE3Floors[resRow[clueAreaColumn]][resRow[usageColumn]][resRow[yearColumn]] += int(resRow[floorsColumn])

					collatedCLUE4[resRow[clueAreaColumn]][int(resRow[blockIdColumn])][resRow[usageColumn]][resRow[yearColumn]] += 1
					collatedCLUE4Floors[resRow[clueAreaColumn]][int(resRow[blockIdColumn])][resRow[usageColumn]][resRow[yearColumn]] += int(resRow[floorsColumn])

					prev = collatedCLUE4MaxFloors[resRow[clueAreaColumn]][int(resRow[blockIdColumn])][resRow[usageColumn]][resRow[yearColumn]]
					collatedCLUE4MaxFloors[resRow[clueAreaColumn]][int(resRow[blockIdColumn])][resRow[usageColumn]][resRow[yearColumn]] = max(prev, int(resRow[floorsColumn]))

				#output.writerow(resRow)

		#for k, v in collatedCLUE3.keys()

		outfile.write(str(collatedCLUE3).replace('}', "}\n").replace('{', "{\n").replace(',', ",\n\t").replace("defaultdict(<class 'int'>,", ""))
		
		print(len(collatedCLUE))
		block8 = collatedCLUE2['8']
		print(sorted(block8.items()))

	with open("cleaned3.csv", "w", newline="") as outfile:
		clueAreaIdToName = json.load(open("CLUE_index_to_region.json"))["map"]
	
		colArray = [
			"CLUESmallArea",
			"CensusYear",
			"BuildingCount"
			"AverageFloors"
		]
	
		output = csv.writer(outfile)
		output.writerow(colArray)
		for k in collatedCLUE2.keys():
			for y in collatedCLUE2[k].keys():
				output.writerow([clueAreaIdToName[int(k)], y, collatedCLUE2[k][y], collatedCLUE2Floors[k][y]/collatedCLUE2[k][y]])

	with open("cleaned4.csv", "w", newline="") as outfile:
		clueAreaIdToName = json.load(open("CLUE_index_to_region.json"))["map"]
	
		colArray = [
			"CLUESmallArea",
			"ChangeInAverageFloors"
		]
	
		output = csv.writer(outfile)
		output.writerow(colArray)
		for k in collatedCLUE2.keys():
			output.writerow(
				[
					clueAreaIdToName[int(k)],
					(collatedCLUE2Floors[k]["2021"]/collatedCLUE2[k]["2021"]) / (collatedCLUE2Floors[k]["2002"]/collatedCLUE2[k]["2002"]) - 1
				]
			)
			
	with open("cleaned5.csv", "w", newline="") as outfile:
		clueAreaIdToName = json.load(open("CLUE_index_to_region.json"))["map"]
		usageIdToName = json.load(open("Index_to_predominant_space_use.json"))["map"]
	
		colArray = [
			"CLUESmallArea",
			"Usage",
			"SumFloors2002",
			"BuildingCount2002",
			"SumFloors2021"
			"BuildingCount2021",
		]

		"""NOTE: We have to add in empty values when a usage type is missing for an area"""				

		output = csv.writer(outfile)
		output.writerow(colArray)
		for k1 in collatedCLUE3.keys():
			for usageKey in collatedCLUE3[k1].keys():
				output.writerow(
					[
						clueAreaIdToName[int(k1)],
						usageIdToName[int(usageKey)],
						collatedCLUE3Floors[k1][usageKey]["2002"],
						collatedCLUE3[k1][usageKey]["2002"],
						collatedCLUE3Floors[k1][usageKey]["2021"],
						collatedCLUE3[k1][usageKey]["2021"]
					]
				)
			for usageKey in [0, 2, 3, 4, 16]: #One key from each usage class, so we don't have missing values on the map
				if str(usageKey) in list(collatedCLUE3[k1].keys()):
					continue
				output.writerow(
					[
						clueAreaIdToName[int(k1)],
						usageIdToName[int(usageKey)],
						0,
						0,
						0,
						0
					]
				)

	with open("cleaned6.csv", "w", newline="") as outfile:
		clueAreaIdToName = json.load(open("CLUE_index_to_region.json"))["map"]
		usageIdToName = json.load(open("Index_to_predominant_space_use.json"))["map"]
	
		colArray = [
			"CLUESmallArea",
			"BlockId",
			"Usage",
			"SumFloors2002",
			"BuildingCount2002",
			"SumFloors2021",
			"BuildingCount2021",
			"MostFloors2002",
			"MostFloors2021"
		]

		"""NOTE: We have to add in empty values when a usage type is missing for a BlockId"""				

		output = csv.writer(outfile)
		output.writerow(colArray)
		for k1 in collatedCLUE4.keys():
			for blockIdKey in collatedCLUE4[k1].keys():
				for usageKey in collatedCLUE4[k1][blockIdKey].keys():
					output.writerow(
						[
							clueAreaIdToName[int(k1)],
							int(blockIdKey),
							usageIdToName[int(usageKey)],
							collatedCLUE4Floors[k1][blockIdKey][usageKey]["2002"],
							collatedCLUE4[k1][blockIdKey][usageKey]["2002"],
							collatedCLUE4Floors[k1][blockIdKey][usageKey]["2021"],
							collatedCLUE4[k1][blockIdKey][usageKey]["2021"],
							collatedCLUE4MaxFloors[k1][blockIdKey][usageKey]["2002"],
							collatedCLUE4MaxFloors[k1][blockIdKey][usageKey]["2021"],
						]
					)
				for usageKey in [0, 2, 3, 4, 16]: #One key from each usage class, so we don't have missing values on the map
					if str(usageKey) in list(collatedCLUE4[k1][blockIdKey].keys()):
						continue
					output.writerow(
						[
							clueAreaIdToName[int(k1)],
							blockIdKey,
							usageIdToName[int(usageKey)],
							0,
							0,
							0,
							0
						]
					)
	

def main():
	cleanPass2()

if __name__ == "__main__":
	main()
