# Dbus service file
servicedir = $(DBUS_SERVICES_DIR)
service_in_files = mousetracker.daemon.service.in
service_DATA = $(service_in_files:.service.in=.service)
DISTCLEANFILES = $(service_DATA)
EXTRA_DIST = $(service_in_files)

# Rule to make the service file with bindir expanded
$(service_DATA): $(service_in_files) Makefile
	sed  "s|@serviceprogramdir@|$(bindir)|" $<> $@

