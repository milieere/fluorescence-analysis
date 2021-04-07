	//roi1 small
function process(file) { 
	prevNumResults = nResults;  
	open(file);
	original = getTitle();
	run("Duplicate...", " ");

	run("Smooth");
	run("Subtract Background...", "rolling=5");
	setOption("ScaleConversions", true);
	run("8-bit");
	run("Auto Local Threshold", "method=Mean radius=5 parameter_1=-10 parameter_2=0 white");
	run("Create Selection");
	run("ROI Manager...");
	roiManager("Add");


	///roi2 big
	selectWindow(original);
	run("Duplicate...", " ");

	run("Smooth");
	run("Subtract Background...", "rolling=30");
	setOption("ScaleConversions", true);
	run("8-bit");
	run("Auto Local Threshold", "method=Mean radius=30 parameter_1=-60 parameter_2=0 white");
	run("Create Selection");
	run("ROI Manager...");
	roiManager("Add");

	mask_1 = roiManager("count")-2;
	mask_2 = roiManager("count")-1;
	roiManager("Select", newArray(mask_1,mask_2));
	roiManager("Combine");
	roiManager("Add");
	mask = roiManager("count")-1;



	selectWindow(original);

	roiManager("Select", mask);
	run("Measure");
	

// Now loop through each of the new results, and add the filename to the "Filename" column
    for (row = prevNumResults; row < nResults; row++)
    {
        setResult("filename", row, original);
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