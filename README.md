campaign_lobby-state-AK
=========================
Installation
------------

<h4>Requirements</h4>
<blockquote> pip -r install requirements.txt </blockquote>

<h4>Do Not Edit the config.py</h4>
You should  instead edit the config_local.py where you can overwrite(if nescessary) the following 3 variables:<br>
<b>DOWNLOAD_DIR</b> is the directory that the unzipped EXE files will be downloaded to.<br>
<b>TEXT_CONV</b> is the directory that the downloaded EXE files will be extracted to. I make this directory a subdirectory of the <em>download_dir</em> - see above.<br>
<b>DATA_DIR</b> is the directory that the final json files will be distributed to.  




To Use 
------
<blockquote>python run.py -p<print>|-d<download>|-r<report> & optional_Filter_String</blockquote>

Example print:
<blockquote><b>python run.py -p</b> <i> - prints all  files names and url pdf links.</i></blockquote>

<blockquote><b>python run.py -p 2009</b> 
<i>- prints all the names and urls of all files with "2009" in the name.</i></blockquote>


Example download:
<blockquote><b>python run.py -d </b><i> - downloads all pdf files, converts to text distributes 1 json file per text record. The json files are saved to Year (and a sub "reimburse" Folders. The Year folders are created during this process.</i></blockquote>   
<blockquote><b>python run.py -d 2009</b><i>
Downloads only files with "2009" in the name.</i></blockquote> 

Notes
-----
You can run a report with the <b>-r</b> flag . The report breaks down the counts of files in each lowest level subdirectory.  
<blockquote> python run.py -r 2009 </blockquote>  

<h5>Directory Structure </h5>
If you do not override the config.py default directories the the directory structure(shown at the end of the README)
will be created within the campaign-finance_state_OH directory.
If you do override the config.py variables then remember to change the USE_ALTERNATE variable to True.

<h5>Bad Dates</h5>
There is a bad_data file provided in every Year folder.
The bad data are mostly(if not all) missing fee amounts 

<h5>Files That Are Used</h5>
Currently there are files excluded from this process. Specifically files that break the data by Employer. THere is only a SchedB field that is non redundent. If someone wants the schedB field then 
you will need to request it and we can see about including it.

TODO
----
<ul>
<li>Find out if some files I am excluding are in fact relevant</li>
<li>Test a full download and address the inevitable errors.</li>
<li>Unit tests.</li>
<li>refactor</li>
</ul>


Example Directory structure: run.py -d 2011 && run.py -d 2010
-------------------------------------------

    
    data
    ├── 2010
    │   └── reimburse
    └── 2011
        └── reimburse
    
