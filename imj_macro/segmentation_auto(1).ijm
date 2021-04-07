function process(file) { 
	prevNumResults = nResults;  
	open(file);
	filename = getTitle();

	run("Duplicate...", " ");

	run("Remove Outliers...", "radius=10 threshold=1 which=Bright");
	run("Median...", "radius=10");
	run("Subtract Background...", "rolling=120");
	setOption("ScaleConversions", true);
	run("8-bit");
	run("Auto Local Threshold", "method=Mean radius=120 parameter_1=-4 parameter_2=0 white");
	run("Invert LUT");
	run("Create Selection");
	run("ROI Manager...");
	roiManager("Add");

	mask = roiManager("count")-1;

	selectWindow(filename);

	roiManager("Select", mask);
	run("Measure");

	// Now loop through each of the new results, and add the filename to the "Filename" column
    for (row = prevNumResults; row < nResults; row++)
    {
        setResult("Filename", row, filename);
    }


}

setBatchMode(true); 

inputDirectory = getDirectory("Choose a Directory of Images");

fileList = getFileList(inputDirectory);

for (i = 0; i < fileList.length; i++)
{
    process(fileList[i]);
}

setBatchMode(false); 
updateResults();  