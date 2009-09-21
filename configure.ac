AC_INIT(MouseTracker, 0.0.1, ruiandrebatista@gmail.com)
AM_INIT_AUTOMAKE
AM_MAINTAINER_MODE

dnl d-bus service stuff
AS_AC_EXPAND(DATADIR, $datadir)

DBUS_SERVICES_DIR="$DATADIR/dbus-1/services"
AC_SUBST(DBUS_SERVICES_DIR)
AC_DEFINE_UNQUOTED(DBUS_SERVICES_DIR, "$DBUS_SERVICES_DIR", [Where services dir for DBUS is])

dnl == Check for install ==
AC_PROG_INSTALL


dnl == check for python ==
AM_PATH_PYTHON(2.4)

dnl == check for gstreamer ==
#PKG_CHECK_MODULES(MOUSETRACKER, gstreamer-0.10 gst-python-0.10 dbus-python)


#dnl == i18n ==
#GETTEXT_PACKAGE=mousetracker
#AC_SUBST(GETTEXT_PACKAGE)
#AC_DEFINE_UNQUOTED(GETTEXT_PACKAGE, "$GETTEXT_PACKAGE", [The gettext package])
#AM_GLIB_GNU_GETTEXT

#dnl == intltool check ==
#IT_PROG_INTLTOOL([0.35.0])

dnl == generate makefiles ==
AC_OUTPUT([
Makefile
data/Makefile
data/mousetracker.daemon.service
src/Makefile
src/mousetracker/Makefile
src/mousetracker/mousetracker
src/mousetracker/_constants.py
])
