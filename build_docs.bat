rmdir docs
move main.py SphinxDocs
sphinx-apidoc . -o ./SphinxDocs/source -f
cd SphinxDocs
move main.py ..
call make.bat html
cd ..
Xcopy /E /I .\SphinxDocs\build\html .\docs /y
rmdir /Q /S SphinxDocs\build
fsutil file createnew docs/.nojekyll 0