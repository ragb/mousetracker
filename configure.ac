AC_INIT(MouseTRacker, 0.0.1, ruiandrebatista@gmail.com)
AM_INIT_AUTOMAKE
AM_MAINTAINER_MODE


dnl == check for gstreamer ==
PKG_CHECK_MODULES(GSTREAMER, gstreamer-0.10)


dnl == Check for install ==
AC_PROG_INSTALL

dnl == check for python ==
AM_PATH_PYTHON(2.4)

dnl check for python modules
#AM_CHECK_PYGTK(2.0,,[AC_MSG_ERROR(Could not find pygtk 2.0)])
#AM_CHECK_PYMOD(gobject,,,[AC_MSG_ERROR(Could not find python module: gobject)])
#AM_CHECK_PYMOD(pyatspi,,,[AC_MSG_ERROR(Could not find python module: pyatspi)])
#AM_CHECK_PYMOD(pygst,,,[AC_MSG_ERROR(Could not find python module: pygst)])

dnl == i18n ==
#GETTEXT_PACKAGE=mouselocator
#AC_SUBST(GETTEXT_PACKAGE)
#AC_DEFINE_UNQUOTED(GETTEXT_PACKAGE, "$GETTEXT_PACKAGE", [The gettext package])
#AM_GLIB_GNU_GETTEXT

dnl == intltool check ==
#IT_PROG_INTLTOOL([0.35.0])

dnl == generate makefiles ==
AC_OUTPUT([
Makefile
src/Makefile
src/mousetracker/Makefile
])
