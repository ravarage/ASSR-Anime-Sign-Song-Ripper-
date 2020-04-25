<a href="https://github.com/ravarage/ASSR-Anime-Sign-Song-Ripper-/releases"><h1>ASSR(Anime Sign&Songs Subtitle Creater)</h1></a><br>
<label class="center" >Software design to Create Sign&Songs subtitle from ASS(SubStation Alpha) for Anime from Main Subtitle</label>
<p align="middle"><img  src="https://i.postimg.cc/WpGRKMZ6/main-w-DTp-Lug-RFN.png" alt="ASSR" align="middle" height="450" width="800"></p>
<h2>Program Feature</h2>
<ul>
    <li>It can create Sign&Song Subtitle from Main ASS(SubStation Alpha)</li>
    <li>It can extract main subtitle from mkv files</li>
    <li>It can merge new subtitle with mkv files</li>
    <li>It can view lines with selected tags(experimental)</li>
</ul>
<h2>Usage</h2><img src="https://i.postimg.cc/cJLtfhbC/main-9-Hk-WNJNRav.png" alt="TvNaming" align="right" height="150" width="300"><br>
<h3>For ASS(SubStation Alpha) Files</h3>
<ol>
    <li>Load the Ass Files</li>
    <li>Double Click on files to view where the Tag have been used</li>
    <li>Click Tag to remove to remove the lines with certain tags</li>
    <li>Start Ripping</li>
    <li>Get your new file in folder called out next to source file
    <ul>
        <li>Doing whole season depending on Anime(most of the time is fine) it can lead to false detection avoid it when anime have too much tags</li>
    </ul></li>
</ol>
<code>for MKV files its some procedure except you need to have MKVToolnix and FFprobe on your computer so you can read, extract and merge the new subtitle </code>
<h2>Coding details</h2>
<ul>
    <li>The Software Written in Python</li>
    <li>Library Used PYQT5(GUI),MPV and PySub2</li>
    <li>Free and Open Source</li>
    <li>Windows Binary made Using Nutika with Mingw64</li>
    <li>to Work with mkv files you need to have MKVToolnix and FFprobe</li>
</ul>
<h2>Known Bugs</h2>
<ul>
    <li>Nothin that I know of</li>
</ul>
<h2>ToDO</h2>
<ul>
    <li>Add Linux Support</li>
    <li>ReVamp UI</li>
    <li>More User Settings</li>
</ul>
<h2>ChangeLogs</h2>
<h4>Version 1.0.7</h4>
<ul>
    <li>Fixing Issue1 the app not starting https://github.com/ravarage/ASSR-Anime-Sign-Song-Ripper-/issues/1</li>
    <li>when you load a file it rescan all the loaded files, now it only scan new files</li>
</ul>
<h4>Version 1.0.6</h4>
<ul>
    <li>Text browser now support playing video with mpv using libmpv</li>
</ul>
<h4>Version 1.0.5</h4>
<ul>
    <li>Use pysub2 instead of my regex, as its much more accurate than my regex</li>
    <li>improvement of tag recognition as I use pysub2 now, it should be almost perfect</li>
    <li>fixed issue in batch</li>
    <li>fixed issue in tag text viewer</li>
    <li>better Installer, better inno installer script used to make installer</li>
</ul>
<h4>Version 1.0.4</h4>
<ul>
    <li>Windows path limitation had been fixed</li>
    <li>improvement of tag recognition</li>
</ul>
<h4>Version 1.0.3</h4>
<ul>
    <li>Now we have proper progress bar no more console shell.</li>
    <li>Tag Explore, you can double click on a file it will open a window so you can read what lines written using that tag(experimental)</li>
</ul>
<h4>Version 1.0.2</h4>
<ul>
    <li>Improved Accuracy recognizing tags, better recognition of what to keep and remove.</li>
    <li>Minor bug fixes</li>
</ul>
<h4>Version 1.0.1</h4>
<ul>
    <li>more Accurate recognizing tags, better recognition of what to keep and remove.</li>
    <li>mkv extract now shell will be visible so do not add a tag to remove till mkvextract shell is done(usually takes few seconds)</li>
    <li>the output will be in folder output next to the input file</li>
    <li>it will show you if mkvtoolnix and ffprobe is missing</li>
</ul>

<h4>Version 1.0.0</h4>
<ul>
    <li>Initial release</li>
</ul>
<label>***Icon taken from flaticons ***</label>
