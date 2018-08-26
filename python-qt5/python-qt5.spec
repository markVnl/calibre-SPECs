
%if 0%{?fedora} || 0%{?rhel} > 7
%global with_python3 1
%global python3_dbus_dir %(%{__python3} -c "import dbus.mainloop; print(dbus.mainloop.__path__[0])" 2>/dev/null)
%endif
%global with_python2 1
%global python2_dbus_dir %(%{__python2} -c "import dbus.mainloop; print(dbus.mainloop.__path__[0])" 2>/dev/null)

# enable/disable individual modules
# drop power64, it's not supported yet (than)
%if 0%{?fedora} || 0%{?rhel} > 7
%ifarch %{?qt5_qtwebengine_arches}%{?!qt5_qtwebengine_arches:%{ix86} x86_64 %{arm} aarch64 mips mipsel mips64el}
%global webengine 1
%endif
%endif
%global webkit 1

%global rpm_macros_dir %(d=%{_rpmconfigdir}/macros.d; [ -d $d ] || d=%{_sysconfdir}/rpm; echo $d)

Summary: PyQt5 is Python bindings for Qt5
Name:    python-qt5 
Version: 5.9.1
Release: 3%{?dist}

# all BSD, except for GPLv2+ dbus bindings and examples
License: BSD and GPLv2+
Url:     http://www.riverbankcomputing.com/software/pyqt/
%if 0%{?snap:1}
Source0: http://www.riverbankcomputing.com/static/Downloads/PyQt5/PyQt5_gpl-%{version}%{?snap:-snapshot-%{snap}}.tar.gz
%else
Source0: http://downloads.sourceforge.net/project/pyqt/PyQt5/PyQt-%{version}/PyQt5_gpl-%{version}.tar.gz
%endif
Source1: macros.pyqt5
# wrapper, see https://bugzilla.redhat.com/show_bug.cgi?id=1193107#c9
Source2: pylupdate5.sh
Source3: pyrcc5.sh
Source4: pyuic5.sh

## upstream patches

## upstreamable patches
Patch0: python-qt5_sipdir.patch
# support newer Qt5 releases than just 5.9.3
Patch1: PyQt5-Timeline.patch

BuildRequires: chrpath
BuildRequires: findutils
BuildRequires: pkgconfig(dbus-1)
BuildRequires: pkgconfig(dbus-python)
BuildRequires: pkgconfig(phonon4qt5)
BuildRequires: pkgconfig(Qt5Core) >= 5.5
BuildRequires: pkgconfig(Enginio)
BuildRequires: pkgconfig(Qt5Bluetooth)
BuildRequires: pkgconfig(Qt5DBus)
BuildRequires: pkgconfig(Qt5Designer)
BuildRequires: pkgconfig(Qt5Gui)
BuildRequires: pkgconfig(Qt5Location)
BuildRequires: pkgconfig(Qt5Multimedia) pkgconfig(libpulse-mainloop-glib)
BuildRequires: pkgconfig(Qt5Nfc)
BuildRequires: pkgconfig(Qt5Network) pkgconfig(Qt5OpenGL)
BuildRequires: pkgconfig(Qt5Positioning)
BuildRequires: pkgconfig(Qt5Quick) pkgconfig(Qt5QuickWidgets)
BuildRequires: pkgconfig(Qt5Script)
BuildRequires: pkgconfig(Qt5Sensors)
BuildRequires: pkgconfig(Qt5SerialPort)
BuildRequires: pkgconfig(Qt5Sql) pkgconfig(Qt5Svg) pkgconfig(Qt5Test)
BuildRequires: pkgconfig(Qt5X11Extras)
BuildRequires: pkgconfig(Qt5Xml) pkgconfig(Qt5XmlPatterns)
BuildRequires: pkgconfig(Qt5WebChannel)
BuildRequires: pkgconfig(Qt5WebSockets)
BuildRequires: python2-devel python2
BuildRequires: sip-devel >= 4.19.4
%if 0%{?with_python3}
BuildRequires: python3-devel python3
BuildRequires: python3-sip-devel >= 4.19.4
BuildRequires: python3-dbus
%endif # with_python3

# when split out
%if 0%{?webengine} || 0%{?webkit}
Obsoletes: python-qt5 < 5.5.1-10
%endif

Requires: %{name}-base%{?_isa} = %{version}-%{release}
BuildRequires: qt5-qtbase-private-devel
%{?_qt5:Requires: %{_qt5}%{?_isa} = %{_qt5_version}}
%{?_sip_api:Requires: sip-api(%{_sip_api_major}) >= %{_sip_api}}

%global __provides_exclude_from ^(%{python2_sitearch}/.*\\.so|%{python3_sitearch}/.*\\.so|%{_qt5_plugindir}/.*\\.so)$

Provides: PyQt5 = %{version}-%{release}
Provides: PyQt5%{?_isa} = %{version}-%{release}
Provides: python2-PyQt5 = %{version}-%{release}
Provides: python2-PyQt5%{?_isa} = %{version}-%{release}
Provides: python2-qt5 = %{version}-%{release}
Provides: python2-qt5%{?_isa} = %{version}-%{release}

%description
PyQt5 is Python bindings for Qt5.

%package base
Summary: Python bindings for Qt5 base
Requires: %{name}-rpm-macros = %{version}-%{release}
Requires: dbus-python
Obsoletes: python-qt5 < 5.5.1-10
%description base

%package devel
Summary: Development files for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: qt5-qtbase-devel
Requires: sip-devel
Provides: PyQt5-devel = %{version}-%{release}
Provides: python2-PyQt5-devel = %{version}-%{release}
%description devel
Files needed to build other bindings for C++ classes that inherit from any
of the Qt5 classes

%package rpm-macros
Summary: RPM macros %{name}
# when split out
Conflicts: python-qt5 < 5.6
Conflicts: python3-qt5 < 5.6
BuildArch: noarch
%description rpm-macros
%{summary}.

%package -n python3-qt5
Summary: Python 3 bindings for Qt5
%{?_qt5:Requires: %{_qt5}%{?_isa} = %{_qt5_version}}
%{?_sip_api:Requires: python3-sip-api(%{_sip_api_major}) >= %{_sip_api}}
# when split out
%if 0%{?webengine} || 0%{?webkit}
Obsoletes: python3-qt5 < 5.5.1-10
%endif
Provides: python3-PyQt5 = %{version}-%{release}
Provides: python3-PyQt5%{?_isa} = %{version}-%{release}
Requires: python3-qt5-base%{?_isa} = %{version}-%{release}
%description -n python3-qt5
%{summary}.

%package -n python3-qt5-base
Summary: Python 3 bindings for Qt5 base
%{?_qt5:Requires: %{_qt5}%{?_isa} = %{_qt5_version}}
%{?_sip_api:Requires: python3-sip-api(%{_sip_api_major}) >= %{_sip_api}}
Provides: python3-PyQt5-base = %{version}-%{release}
Provides: python3-PyQt5-base%{?_isa} = %{version}-%{release}
Requires: %{name}-rpm-macros = %{version}-%{release}
Requires: python3-dbus
%description -n python3-qt5-base
%{summary}.

%package -n python3-qt5-devel
Summary: Development files for python3-qt5
Requires: python3-qt5%{?_isa} = %{version}-%{release}
Requires: qt5-qtbase-devel
Requires: python3-sip-devel
Provides: python3-PyQt5-devel = %{version}-%{release}
%description -n python3-qt5-devel
Files needed to build other bindings for C++ classes that inherit from any
of the Qt5 classes

%package doc
Summary: Developer documentation for %{name} 
Provides: PyQt5-doc = %{version}-%{release}
BuildArch: noarch
%description doc
%{summary}.

%if 0%{?webengine}
%package webengine
Summary: Python bindings for Qt5 WebEngine
BuildRequires: pkgconfig(Qt5WebEngine)
Obsoletes: python-qt5 < 5.5.1-10
Requires:  %{name}%{?_isa} = %{version}-%{release}
%description webengine
%{summary}.

%package -n python3-qt5-webengine
Summary: Python3 bindings for Qt5 WebEngine
Obsoletes: python3-webengine < 5.5.1-13
Obsoletes: python3-qt5 < 5.5.1-10
Requires:  python3-qt5%{?_isa} = %{version}-%{release}
%description -n python3-qt5-webengine
%{summary}.
%endif

%if 0%{?webkit}
%package webkit
Summary: Python bindings for Qt5 Webkit
BuildRequires: pkgconfig(Qt5WebKit) pkgconfig(Qt5WebKitWidgets)
Obsoletes: python3-webkit < 5.5.1-12
Obsoletes: python-qt5 < 5.5.1-10
Requires:  %{name}%{?_isa} = %{version}-%{release}
%description webkit
%{summary}.

%package -n python3-qt5-webkit
Summary: Python3 bindings for Qt5 Webkit
Obsoletes: python3-qt5 < 5.5.1-10
Requires:  python3-qt5%{?_isa} = %{version}-%{release}
%description -n python3-qt5-webkit
%{summary}.
%endif


%prep
%setup -q -n PyQt5_gpl-%{version}%{?snap:-snapshot-%{snap}}

%patch0 -p1
%patch1 -p1


%build
PATH=%{_qt5_bindir}:$PATH ; export PATH

# Python 2 build:
%if 0%{?with_python2}
mkdir %{_target_platform}
# copy sources, seems pure shadow build support broke with 5.9 -- rex
cp -a * %{_target_platform}/ ||:
pushd %{_target_platform}
%{__python2} ./configure.py \
  --assume-shared \
  --confirm-license \
  --qmake=%{_qt5_qmake} \
  --qsci-api --qsci-api-destdir=%{_qt5_datadir}/qsci \
  --verbose \
  QMAKE_CFLAGS_RELEASE="%{optflags}" \
  QMAKE_CXXFLAGS_RELEASE="%{optflags}" \
  QMAKE_LFLAGS_RELEASE="%{?__global_ldflags}"

make %{?_smp_mflags}
popd
%endif # with_python2

# Python 3 build:
%if 0%{?with_python3}
mkdir %{_target_platform}-python3
cp -a * %{_target_platform}-python3/ ||:
pushd %{_target_platform}-python3
%{__python3} ./configure.py \
  --assume-shared \
  --confirm-license \
  --qmake=%{_qt5_qmake} \
  --no-qsci-api \
  --sip=%{_bindir}/python3-sip \
  --verbose \
  QMAKE_CFLAGS_RELEASE="%{optflags}" \
  QMAKE_CXXFLAGS_RELEASE="%{optflags}" \
  QMAKE_LFLAGS_RELEASE="%{?__global_ldflags}"

make %{?_smp_mflags}
popd
%endif # with_python3


%install

# Python 3 build:
%if 0%{?with_python3}
make install DESTDIR=%{buildroot} INSTALL_ROOT=%{buildroot} -C %{_target_platform}-python3
# ensure .so modules are executable for proper -debuginfo extraction
for i in %{buildroot}%{python3_sitearch}/PyQt5/*.so %{buildroot}%{python3_dbus_dir}/pyqt5.so ; do
chmod a+rx $i
done
%endif # with_python3

# Python 2 build:
%if 0%{?with_python2}
make install DESTDIR=%{buildroot} INSTALL_ROOT=%{buildroot} -C %{_target_platform}
# ensure .so modules are executable for proper -debuginfo extraction
for i in %{buildroot}%{python2_sitearch}/PyQt5/*.so %{buildroot}%{python2_dbus_dir}/pyqt5.so ; do
chmod a+rx $i
done
%endif # with_python2

# remove Python3 code from Python2 directory, fixes FTBFS like PyQt4 (#564633)
rm -rfv %{buildroot}%{python2_sitearch}/PyQt5/uic/port_v3/
# remove Python2 code from Python3 directory (for when/if we support python3 here)
rm -rfv %{buildroot}%{python3_sitearch}/PyQt5/uic/port_v2/

# rpm macros
install -p -m644 -D %{SOURCE1} \
  %{buildroot}%{rpm_macros_dir}/macros.pyqt5
sed -i \
  -e "s|@@NAME@@|%{name}|g" \
  -e "s|@@EPOCH@@|%{?epoch}%{!?epoch:0}|g" \
  -e "s|@@VERSION@@|%{version}|g" \
  -e "s|@@EVR@@|%{?epoch:%{epoch:}}%{version}-%{release}|g" \
  %{buildroot}%{rpm_macros_dir}/macros.pyqt5

%if 0%{?with_python3}
# install wrappers to handle both/either python2/python3
# TODO: consider alternatives? -- rex
rm -fv %{buildroot}%{_bindir}/{pyrcc5,pylupdate5,pyuic5}
install -p -m755 -D %{SOURCE2} %{buildroot}%{_bindir}/pylupdate5
install -p -m755 -D %{SOURCE3} %{buildroot}%{_bindir}/pyrcc5
install -p -m755 -D %{SOURCE4} %{buildroot}%{_bindir}/pyuic5
sed -i \
  -e "s|@PYTHON3@|%{__python3}|g" \
  -e "s|@PYTHON2@|%{__python2}|g" \
  %{buildroot}%{_bindir}/{pyrcc5,pylupdate5,pyuic5}
%endif


%if 0%{?with_python2}
%files
%{_qt5_plugindir}/PyQt5/
%{python2_sitearch}/PyQt5/Enginio.so
%{python2_sitearch}/PyQt5/QtBluetooth.so
%{python2_sitearch}/PyQt5/QtDesigner.so
%{python2_sitearch}/PyQt5/QtHelp.so
%{python2_sitearch}/PyQt5/QtLocation.so
%{python2_sitearch}/PyQt5/QtMultimedia.so
%{python2_sitearch}/PyQt5/QtMultimediaWidgets.so
%{python2_sitearch}/PyQt5/QtNfc.so
%{python2_sitearch}/PyQt5/QtPositioning.so
%{python2_sitearch}/PyQt5/QtQml.so
%{python2_sitearch}/PyQt5/QtQuick.so
%{python2_sitearch}/PyQt5/QtQuickWidgets.so
%{python2_sitearch}/PyQt5/QtSensors.so
%{python2_sitearch}/PyQt5/QtSerialPort.so
%{python2_sitearch}/PyQt5/QtSvg.so
%{python2_sitearch}/PyQt5/QtWebChannel.so
%{python2_sitearch}/PyQt5/QtWebSockets.so
%{python2_sitearch}/PyQt5/QtX11Extras.so
%{python2_sitearch}/PyQt5/QtXmlPatterns.so
%{python2_sitearch}/PyQt5/uic/
%{_qt5_plugindir}/designer/libpyqt5.so
# *was* in -devel
%{_bindir}/pylupdate5
%{_bindir}/pyrcc5
%{_bindir}/pyuic5
%{python2_sitearch}/PyQt5/pylupdate.so
%{python2_sitearch}/PyQt5/pylupdate_main.py*
%{python2_sitearch}/PyQt5/pyrcc.so
%{python2_sitearch}/PyQt5/pyrcc_main.py*

%files base
%doc NEWS README
%license LICENSE
%{python2_dbus_dir}/pyqt5.so
%dir %{python2_sitearch}/PyQt5/
%{python2_sitearch}/PyQt5/__init__.py*
%{python2_sitearch}/PyQt5/Qt.so
%{python2_sitearch}/PyQt5/QtCore.so
%{python2_sitearch}/PyQt5/QtDBus.so
%{python2_sitearch}/PyQt5/QtGui.so
%{python2_sitearch}/PyQt5/QtNetwork.so
%{python2_sitearch}/PyQt5/QtOpenGL.so
%{python2_sitearch}/PyQt5/QtPrintSupport.so
%{python2_sitearch}/PyQt5/QtSql.so
%{python2_sitearch}/PyQt5/QtTest.so
%{python2_sitearch}/PyQt5/QtWidgets.so
%{python2_sitearch}/PyQt5/QtXml.so
%{python2_sitearch}/PyQt5/_QOpenGLFunctions_2_0.so
%{python2_sitearch}/PyQt5/_QOpenGLFunctions_2_1.so
%{python2_sitearch}/PyQt5/_QOpenGLFunctions_4_1_Core.so

%if 0%{?webengine}
%files webengine
%{python2_sitearch}/PyQt5/QtWebEngine.*
%{python2_sitearch}/PyQt5/QtWebEngineCore.*
%{python2_sitearch}/PyQt5/QtWebEngineWidgets.*
%endif

%if 0%{?webkit}
%files webkit
%{python2_sitearch}/PyQt5/QtWebKit.*
%{python2_sitearch}/PyQt5/QtWebKitWidgets.*
%endif

%files rpm-macros
%{rpm_macros_dir}/macros.pyqt5

%files devel
%{_datadir}/sip/PyQt5/
%endif

%if 0%{?with_python3}
%files -n python3-qt5
%{python3_sitearch}/PyQt5/Enginio.*
%{python3_sitearch}/PyQt5/QtBluetooth.*
%{python3_sitearch}/PyQt5/QtDesigner.*
%{python3_sitearch}/PyQt5/QtHelp.*
%{python3_sitearch}/PyQt5/QtLocation.*
%{python3_sitearch}/PyQt5/QtMultimedia.*
%{python3_sitearch}/PyQt5/QtMultimediaWidgets.*
%{python3_sitearch}/PyQt5/QtNfc.*
%{python3_sitearch}/PyQt5/QtPositioning.*
%{python3_sitearch}/PyQt5/QtQml.*
%{python3_sitearch}/PyQt5/QtQuick.*
%{python3_sitearch}/PyQt5/QtQuickWidgets.*
%{python3_sitearch}/PyQt5/QtSensors.*
%{python3_sitearch}/PyQt5/QtSerialPort.*
%{python3_sitearch}/PyQt5/QtSvg.*
%{python3_sitearch}/PyQt5/QtWebChannel.*
%{python3_sitearch}/PyQt5/QtWebSockets.*
%{python3_sitearch}/PyQt5/QtX11Extras.*
%{python3_sitearch}/PyQt5/QtXmlPatterns.*
%{python3_sitearch}/PyQt5/uic/
# *was* in python3-qt5-devel
%{_bindir}/pylupdate5
%{_bindir}/pyrcc5
%{_bindir}/pyuic5
%{python3_sitearch}/PyQt5/pylupdate.so
%{python3_sitearch}/PyQt5/pylupdate_main.py*
%{python3_sitearch}/PyQt5/pyrcc.so
%{python3_sitearch}/PyQt5/pyrcc_main.py*

%files -n python3-qt5-base
%doc NEWS README
%license LICENSE
%{python3_dbus_dir}/pyqt5.so
%dir %{python3_sitearch}/PyQt5/
%{python3_sitearch}/PyQt5/__pycache__/
%{python3_sitearch}/PyQt5/__init__.py*
%{python3_sitearch}/PyQt5/Qt.*
%{python3_sitearch}/PyQt5/QtCore.*
%{python3_sitearch}/PyQt5/QtDBus.*
%{python3_sitearch}/PyQt5/QtGui.*
%{python3_sitearch}/PyQt5/QtNetwork.*
%{python3_sitearch}/PyQt5/QtOpenGL.*
%{python3_sitearch}/PyQt5/QtPrintSupport.*
%{python3_sitearch}/PyQt5/QtSql.*
%{python3_sitearch}/PyQt5/QtTest.*
%{python3_sitearch}/PyQt5/QtWidgets.*
%{python3_sitearch}/PyQt5/QtXml.*
%{python3_sitearch}/PyQt5/_QOpenGLFunctions_2_0.*
%{python3_sitearch}/PyQt5/_QOpenGLFunctions_2_1.*
%{python3_sitearch}/PyQt5/_QOpenGLFunctions_4_1_Core.*

%if 0%{?webengine}
%files -n python3-qt5-webengine
%{python3_sitearch}/PyQt5/QtWebEngine.*
%{python3_sitearch}/PyQt5/QtWebEngineCore.*
%{python3_sitearch}/PyQt5/QtWebEngineWidgets.*
%endif

%if 0%{?webkit}
%files -n python3-qt5-webkit
%{python3_sitearch}/PyQt5/QtWebKit.*
%{python3_sitearch}/PyQt5/QtWebKitWidgets.*
%endif

%files -n python3-qt5-devel
%{_datadir}/python3-sip/PyQt5/
%endif # with_python3

%files doc
#doc doc/*
%doc examples/
# avoid dep on qscintilla-python, own %%_qt5_datadir/qsci/... here for now
%dir %{_qt5_datadir}/qsci/
%dir %{_qt5_datadir}/qsci/api/
%dir %{_qt5_datadir}/qsci/api/python/
%doc %{_qt5_datadir}/qsci/api/python/PyQt5.api


%changelog
* Wed Jun 13 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.9.1-3
- branch rebuild (qt5 5.9.6)

* Thu Jan 25 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.9.1-2
- branch rebuild (qt5)
- explicitly support Qt5 newer than just 5.9.3 (+5.9.4,5.10.0,5.10.1)

* Sat Nov 04 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.9.1-1
- 5.9.1

* Mon Oct 09 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.9-8
- rebuild (qt5)

* Fri Sep 29 2017 Troy Dawson <tdawson@redhat.com> - 0.7.19-5
- Cleanup spec file conditionals

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.9-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Mon Jul 31 2017 Florian Weimer <fweimer@redhat.com> - 5.9-5
- Rebuild with binutils fix for ppc64le (#1475636)

* Thu Jul 27 2017 Than Ngo <than@redhat.com> - 5.9-4
- fixed bz#1348507, pyqt5 with python2 in isolated mode

* Wed Jul 26 2017 Than Ngo <than@redhat.com> - 5.9-3
- fixed bz#1348507 - Arbitrary code execution due to insecure loading
  of Python module from CWD

* Wed Jul 19 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.9-2
- rebuild (qt5)

* Wed Jul 05 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.9-1
- PyQt5-5.9

* Wed Jul 05 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.8.2-5
- rebuild (sip)

* Sun May 14 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.8.2-4
- restore -webengine

* Fri May 12 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.8.2-3
- (temp) disable -webengine support

* Thu May 11 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.8.2-2
- rebuild (qt5)

* Mon Apr 03 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.8.2-1
- PyQt5-5.8.2

* Wed Mar 29 2017 Thomas Woerner <twoerner@redhat.com> - 5.8.1-3
- New base sub package to provide QtBase only (RHBZ#1394626)
- New requirement from the main package to the base sub package

* Tue Mar 28 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.8.1-2
- add missing -webengine/-webkit descriptions
- better python3-qt5-devel description

* Tue Mar 07 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.8.1-1
- PyQt5-5.8.1

* Fri Feb 17 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.8-2
- python3-qt5: omit sip files inadvertantly added in 5.7.1-5

* Thu Feb 16 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.8-1
- PyQt5-5.8

* Thu Feb 16 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.7.1-5
- move -devel binaries to main pkg(s) (#1422613)

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.7.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Jan 30 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.7.1-3
- fix pyrcc5 wrapper typo

* Fri Jan 27 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.7.1-2
- add wrappers for pyrcc5,pylupdate5 (#141116,#1415812)
- update provides filtering

* Sat Dec 31 2016 Rex Dieter <rdieter@math.unl.edu> - 5.7.1-1
- PyQt5-5.7.1

* Wed Dec 21 2016 Kevin Fenzi <kevin@scrye.com> - 5.7-6
- Rebuild again for Python 3.6

* Thu Dec 15 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.7-5
- restore qtwebengine support

* Fri Dec 09 2016 Charalampos Stratakis <cstratak@redhat.com> - 5.7-4
- Rebuild for Python 3.6

* Sat Dec 03 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.7-3
- (temporarily) omit webengine support on fc26

* Wed Nov 30 2016 Than Ngo <than@redhat.com> - 5.7-2
- rebuild against new qt5-qtbase-5.7.1

* Tue Jul 26 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.7-1
- PyQt5-5.7

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.6-8
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Sun Jul 17 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.6-7
- enable -webengine on f25+

* Sun Jul 17 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.6-6
- rebuild (qt5-qtbase), disable -webengine (temp on f25, until fixed)

* Wed Jul 06 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.6-5
- BR: qt5-qtbase-private-devel
- python3-qt5: add versioned qt5 dep (like base python-qt5 pkg has)

* Wed Jun 29 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.6-4
- rebuild (qt5)

* Wed Jun 15 2016 Than Ngo <than@redhat.com> - 5.6-3
- drop ppc ppc64 ppc64le, it's not supported yet

* Mon May 02 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.6-2
- -rpm-macros: Conflicts: python(3)-qt5 < 5.6

* Mon Apr 25 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.6-1
- PyQt5-5.6

* Wed Apr 13 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.5.1-20
- rebuild (sip), re-enable -webengine for secondary archs

* Thu Mar 24 2016 Rex Dieter <rdieter@fedoraproject.org> 5.5.1-19
- limit -webengine support to just primary archs (for now)

* Thu Mar 24 2016 Rex Dieter <rdieter@fedoraproject.org> 5.5.1-18
- -rpm-macros subpkg

* Tue Mar 15 2016 Rex Dieter <rdieter@fedoraproject.org> 5.5.1-17
- rebuild (qt5-qtenginio)

* Mon Mar 14 2016 Rex Dieter <rdieter@fedoraproject.org> 5.5.1-16
- -webengine: add ExclusiveArch (matching qt5-qtwebengine's)

* Mon Mar 07 2016 Rex Dieter <rdieter@fedoraproject.org> 5.5.1-15
- add Obsoletes for misnamed -webengine/-webkit pkgs (#1315025)

* Sat Mar 05 2016 Rex Dieter <rdieter@fedoraproject.org> 5.5.1-14
- python-qt5 is not built with $RPM_OPT_FLAGS (#1314998)

* Thu Mar 03 2016 Rex Dieter <rdieter@fedoraproject.org> 5.5.1-13
- fix python3-qt5-webengine name

* Thu Mar 03 2016 Rex Dieter <rdieter@fedoraproject.org> 5.5.1-12
- fix python3-qt5-webkit name

* Wed Mar 02 2016 Rex Dieter <rdieter@fedoraproject.org> 5.5.1-11
- use safer subdir builds

* Wed Mar 02 2016 Rex Dieter <rdieter@fedoraproject.org> 5.5.1-10
- -webengine,-webkit subpkgs

* Sat Feb 27 2016 Christian Dersch <lupinix@mailbox.org> - 5.5.1-9
- Enabled QtWebEngine for Fedora >= 24

* Sat Feb 27 2016 Rex Dieter <rdieter@fedoraproject.org> 5.5.1-8
- rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 5.5.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Feb 01 2016 Rex Dieter <rdieter@fedoraproject.org> 5.5.1-6
- explicitly set CFLAGS,CXXFLAGS,LFLAGS

* Wed Jan 13 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.5.1-5
- %%description: mention PyQt5

* Mon Dec 07 2015 Rex Dieter <rdieter@fedoraproject.org> 5.5.1-4
- rebuild (qt5), Provides: python2-qt5

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.5.1-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Mon Nov 02 2015 Rex Dieter <rdieter@fedoraproject.org> 5.5.1-2
- rebuild (qt5)

* Mon Oct 26 2015 Rex Dieter <rdieter@fedoraproject.org> 5.5.1-1
- 5.5.1
- enable qtenginio, fix pyuic5 wrapper, use %%license

* Mon Oct 12 2015 Rex Dieter <rdieter@fedoraproject.org> 5.5-2
- rebuild (qt5)

* Thu Jul 30 2015 Rex Dieter <rdieter@fedoraproject.org> 5.5-1
- 5.5

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jun 12 2015 Rex Dieter <rdieter@fedoraproject.org> 5.4.2-1
- 5.4.2

* Fri Jun 05 2015 Rex Dieter <rdieter@fedoraproject.org> - 5.4.1-5
- wrong python release used in pyuic5 launch script (#1193107)
- -doc: add qsci doc QyQt5.api content
- enable Qt5WebChannel/Qt5WebSockets support

* Fri Jun 05 2015 Sandro Mani <manisandro@gmail.com> - 5.4.1-4
- Add patch to fix python3 sip installation dir (#1228432)

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 5.4.1-3
- Rebuilt for GCC 5 C++11 ABI change

* Wed Mar 25 2015 Rex Dieter <rdieter@fedoraproject.org> 5.4.1-2
- rebuild (sip)

* Thu Feb 26 2015 Rex Dieter <rdieter@fedoraproject.org> 5.4.1-1
- 5.4.1

* Wed Feb 25 2015 Rex Dieter <rdieter@fedoraproject.org> 5.4-6
- rebuild (sip)

* Tue Jan 06 2015 Rex Dieter <rdieter@fedoraproject.org> 5.4-5
- +macros.pyqt5

* Fri Jan 02 2015 Rex Dieter <rdieter@fedoraproject.org> 5.4-4
- -devel: restore dep on base pkg

* Sun Dec 28 2014 Rex Dieter <rdieter@fedoraproject.org> - 5.4-3
- python3-qt5-devel subpkg

* Sat Dec 27 2014 Rex Dieter <rdieter@fedoraproject.org> 5.4-2
- ensure .so modules are executable (for proper -debuginfo extraction)

* Fri Dec 26 2014 Rex Dieter <rdieter@fedoraproject.org> 5.4-1
- 5.4

* Thu Nov 13 2014 Rex Dieter <rdieter@fedoraproject.org> 5.3.2-6
- restore python3 support

* Tue Nov 11 2014 Rex Dieter <rdieter@fedoraproject.org> 5.3.2-5
- pkgconfig(QtOpenGL) being satisfied by qt4 devel (#1162415)

* Thu Nov 06 2014 Rex Dieter <rdieter@fedoraproject.org> 5.3.2-4
- try to determine dbus-python install paths dynamically (#1161121)

* Thu Nov 06 2014 Rex Dieter <rdieter@fedoraproject.org> - 5.3.2-3
- Build failure in sipQtWebKitWidgestQWebInspector: qprinter.h not found (#1160932)
- python2_sitelib should be python2_sitearch (#1161121)

* Mon Sep 15 2014 Rex Dieter <rdieter@fedoraproject.org> 5.3.2-1
- PyQt-gpl-5.3.2

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jul 06 2014 Rex Dieter <rdieter@fedoraproject.org> 5.3.1-1
- PyQt-gpl-5.3.1

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Jun 02 2014 Rex Dieter <rdieter@fedoraproject.org> 5.3-2
- python3: (Build)Requires: python3-dbus

* Mon Jun 02 2014 Rex Dieter <rdieter@fedoraproject.org> 5.3-1
- PyQt-gpl-5.3
- +Qt5Bluetooth,Qt5Quick,Qt5SerialPorts support

* Mon May 12 2014 Rex Dieter <rdieter@fedoraproject.org> 5.2.1-2
- rebuild (f21-python)
- +Qt5Positioning,Qt5Sensors support

* Sun Mar 16 2014 Rex Dieter <rdieter@fedoraproject.org> 5.2.1-1
- PyQt-5.2.1

* Sat Mar 08 2014 Kevin Kofler <Kevin@tigcc.ticalc.org> 5.2-5
- Rebuild against fixed qt5-qtbase to fix -debuginfo (#1065636)

* Sat Feb 15 2014 Rex Dieter <rdieter@fedoraproject.org> 5.2-4
- python3-qt5 support

* Thu Feb 13 2014 Rex Dieter <rdieter@fedoraproject.org> 5.2-3
- Provides: PyQt5

* Thu Feb 06 2014 Rex Dieter <rdieter@fedoraproject.org> 5.2-2
- BR: python2-devel, use %%__python2 macro

* Wed Jan 08 2014 Rex Dieter <rdieter@fedoraproject.org> 5.2-1
- PyQt-5.2

