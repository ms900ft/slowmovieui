WATCH_FILES= find . -type f -not -path '*/\.*' -not -path '*movieui\/*' | grep -i '.*[.]py\|html$$' 2> /dev/null


entr_warn:
	@echo "----------------------------------------------------------"
	@echo "     ! File watching functionality non-operational !      "
	@echo ""
	@echo "Install entr(1) to automatically run tasks on file change."
	@echo "See http://entrproject.org/"
	@echo "----------------------------------------------------------"



run:
	python slowmovie2.py -w


watch_run:
	if command -v entr > /dev/null; then ${WATCH_FILES} | entr -rc $(MAKE) run; else $(MAKE) run entr_warn; fi