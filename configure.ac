AC_INIT(MouseTracker, 0.0.1, ruiandrebatista@gmail.com)
AM_INIT_AUTOMAKE
AM_MAINTAINER_MODE

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
src/Makefile
src/mousetracker/Makefile
src/mousetracker/mousetracker
src/mousetracker/_constants.py
])
