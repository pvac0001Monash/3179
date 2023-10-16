import csv
import json

def cleanPass1():
	with open("cleaned.csv", "w", newline="") as outfile:

		header = """Census year,Block ID,Property ID,Base property ID,Building name,Street address,CLUE small area,Construction year,Refurbished year,Number of floors (above ground),Predominant space use,Accessibility type,Accessibility type description,Accessibility rating,Bicycle spaces,Has showers,Longitude,Latitude,Location"""
		sHeader = header.split(",")

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

		with open("CLUE_index_to_region.json") as jsFile:
			CLUEMap = json.load(jsFile)["map"]

		clueAreaColumn = list(colMap.keys()).index("CLUE small area")

		with open("Index_to_predominant_space_use.json") as jsFile:
			UsageMap = json.load(jsFile)["map"]

		UsageColumn = list(colMap.keys()).index("Predominant space use")

		with open("buildings-with-name-age-size-accessibility-and-bicycle-facilities.csv") as csvfile:
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

				resRow[clueAreaColumn] = CLUEMap.index(resRow[clueAreaColumn])
				resRow[UsageColumn] = UsageMap.index(resRow[UsageColumn])

				output.writerow(resRow)

def main():
	cleanPass1()

if __name__ == "__main__":
	main()