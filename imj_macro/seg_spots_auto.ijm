function process(file) { 
	prevNumResults = nResults;  
	open(file);
	filename = getTitle();

///low parameter (more negative) 
//and bigger radius - necks and buds and then small radius with less stringent parameter 1
//add the two ROIs

	run("Duplicate...", " ");

	run("Smooth");
	run("Subtract Background...", "rolling=15");
	setOption("ScaleConversions", true);
	run("8-bit");
	run("Auto Local Threshold", "method=Mean radius=15 parameter_1=-20 parameter_2=0 white");
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