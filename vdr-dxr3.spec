%define pname     dxr3
%define plugindir %(vdr-config --plugindir  2>/dev/null || echo ERROR)
%define apiver    %(vdr-config --apiversion 2>/dev/null || echo ERROR)

Name:           vdr-%{pname}
Version:        0.2.10
Release:        1%{?dist}
Summary:        Hollywood+/DXR3 output plugin for VDR

Group:          Applications/Multimedia
License:        GPLv2+
URL:            http://projects.vdr-developer.org/projects/show/plg-dxr3
Source0:        http://projects.vdr-developer.org/attachments/download/162/%{name}-%{version}.tgz
Source1:        %{name}.conf
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  vdr-devel >= 1.4.0
BuildRequires:  em8300-devel
BuildRequires:  ffmpeg-devel
Requires:       vdr(abi) = %{apiver}
Requires:       em8300-kmod >= 0.15.2

%description
This plugin allows using a Hollywood+/DXR3 MPEG decoder card as VDR's
primary output device.


%prep
%setup -q -n %{pname}-%{version}
for f in CONTRIBUTORS HISTORY TROUBLESHOOTING ; do
  iconv -f iso-8859-1 -t utf-8 $f > $f.utf-8 ; mv $f.utf-8 $f
done
%if 0%{?_without_xine_scaler:1}
sed -i -e /-DUSE_XINE_SCALER/d Makefile
%endif


%build
make %{?_smp_mflags} LIBDIR=. VDRDIR=%{_libdir}/vdr \
  FFMDIR=%{_includedir}/ffmpeg LOCALEDIR=%{_tmppath}/%{name}-tmp


%install
rm -rf $RPM_BUILD_ROOT
make i18n LOCALEDIR=$RPM_BUILD_ROOT%{_libdir}/vdr/locale
install -dm 755 $RPM_BUILD_ROOT%{plugindir}
install -pm 755 libvdr-%{pname}.so.%{apiver} $RPM_BUILD_ROOT%{plugindir}
install -Dpm 644 %{SOURCE1} \
  $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/vdr-plugins.d/%{pname}.conf
for l in ca_ES de_DE es_ES fi_FI it_IT pl_PL ; do
  lshort=`echo $l | cut -c -2`
  echo "%lang($lshort) %{_libdir}/vdr/locale/$l/LC_MESSAGES/%{name}.mo" >> %{name}.lang
done


%clean
rm -rf $RPM_BUILD_ROOT


%files -f %{name}.lang
%defattr(-,root,root,-)
%doc CONTRIBUTORS COPYING HISTORY README TROUBLESHOOTING
%config(noreplace) %{_sysconfdir}/sysconfig/vdr-plugins.d/%{pname}.conf
%{plugindir}/libvdr-%{pname}.so.%{apiver}


%changelog
* Sat Jan 02 2010 Felix Kaechele <heffer@fedoraproject.org> - 0.2.10-1
- new upstream release

* Sun Mar 29 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 0.2.8-4
- rebuild for new F11 features

* Sat Dec 20 2008 Dominik Mierzejewski <rpm@greysector.net> - 0.2.8-3
- rebuild against new ffmpeg

* Mon Aug 04 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info - 0.2.8-2
- rebuild

* Tue Apr  8 2008 Ville Skyttä <ville.skytta at iki.fi> - 0.2.8-1
- 0.2.8, new ffmpeg patch applied upstream.
- Build for VDR 1.6.0.

* Wed Aug 22 2007 Ville Skyttä <ville.skytta at iki.fi> - 0.2.7-2
- BuildRequires: gawk for extracting APIVERSION.
- Fix build with > ~2007-07 ffmpeg.
- License: GPLv2+

* Sat May 12 2007 Ville Skyttä <ville.skytta at iki.fi> - 0.2.7-1
- 0.2.7.

* Sun Jan  7 2007 Ville Skyttä <ville.skytta at iki.fi> - 0.2.6-7
- Rebuild for VDR 1.4.5.

* Sat Nov  4 2006 Ville Skyttä <ville.skytta at iki.fi> - 0.2.6-6
- Rebuild for VDR 1.4.4.

* Fri Oct 06 2006 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> 0.2.6-5
- rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Sat Sep 23 2006 Ville Skyttä <ville.skytta at iki.fi> - 0.2.6-4
- Rebuild for VDR 1.4.3.

* Sun Aug  6 2006 Ville Skyttä <ville.skytta at iki.fi> - 0.2.6-3
- Require em8300-kmod, not kmod-em8300.
- Add "--with ac3" rpmbuild option for building with the AC3 patch applied.

* Sun Jun 11 2006 Ville Skyttä <ville.skytta at iki.fi> - 0.2.6-2
- Rebuild for VDR 1.4.1.

* Sun Apr 30 2006 Ville Skyttä <ville.skytta at iki.fi> - 0.2.6-1
- 0.2.6, build for VDR 1.4.0.

* Mon Apr 17 2006 Ville Skyttä <ville.skytta at iki.fi> - 0.2.5-10
- Rebuild/adjust for VDR 1.3.47, require versioned vdr(abi).
- Trim pre-RLO %%changelog entries.

* Sun Mar 26 2006 Ville Skyttä <ville.skytta at iki.fi> - 0.2.5-9
- Rebuild for VDR 1.3.45.

* Sat Mar 18 2006 Ville Skyttä <ville.skytta at iki.fi> - 0.2.5-8
- Don't use %%bcond_without (#814).

* Sat Mar 18 2006 Thorsten Leemhuis <fedora at leemhuis.info> - 0.2.5-7
- drop 0.lvn from release

* Wed Mar  1 2006 Ville Skyttä <ville.skytta at iki.fi> - 0.2.5-0.lvn.7
- Rebuild for VDR 1.3.44.

* Tue Feb 28 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- add dist

* Sun Feb 19 2006 Ville Skyttä <ville.skytta at iki.fi> - 0.2.5-0.lvn.6
- Rebuild for VDR 1.3.43.

* Sun Feb  5 2006 Ville Skyttä <ville.skytta at iki.fi> - 0.2.5-0.lvn.5
- Rebuild/patch for VDR 1.3.42.

* Sun Jan 22 2006 Ville Skyttä <ville.skytta at iki.fi> - 0.2.5-0.lvn.4
- Rebuild for VDR 1.3.40.

* Tue Jan 17 2006 Ville Skyttä <ville.skytta at iki.fi> - 0.2.5-0.lvn.3
- Remove unneeded jpeglib.h inclusion (#733).

* Sun Jan 15 2006 Ville Skyttä <ville.skytta at iki.fi> - 0.2.5-0.lvn.2
- Rebuild for VDR 1.3.39.

* Tue Jan 10 2006 Ville Skyttä <ville.skytta at iki.fi> - 0.2.5-0.lvn.1
- 0.2.5.
- Rebuild for VDR 1.3.38.
- Make build with Xine scaler optional (default to on).

* Thu Jan  5 2006 Ville Skyttä <ville.skytta at iki.fi> - 0.2.4-0.lvn.8
- Rebuild against new ffmpeg.

* Thu Nov 24 2005 Ville Skyttä <ville.skytta at iki.fi> - 0.2.4-0.lvn.7
- Adjust firmware location for em8300 >= 0.15.2, require it.

* Sun Nov  6 2005 Ville Skyttä <ville.skytta at iki.fi> - 0.2.4-0.lvn.6
- Rebuild for VDR 1.3.36.

* Tue Nov  1 2005 Ville Skyttä <ville.skytta at iki.fi> - 0.2.4-0.lvn.5
- Rebuild for VDR 1.3.35.

* Mon Oct  3 2005 Ville Skyttä <ville.skytta at iki.fi> - 0.2.4-0.lvn.4
- Rebuild for VDR 1.3.34.

* Sun Sep 25 2005 Ville Skyttä <ville.skytta at iki.fi> - 0.2.4-0.lvn.3
- Rebuild for VDR 1.3.33.

* Sun Sep 11 2005 Ville Skyttä <ville.skytta at iki.fi> - 0.2.4-0.lvn.2
- Rebuild for VDR 1.3.32.

* Sat Aug 27 2005 Ville Skyttä <ville.skytta at iki.fi> - 0.2.4-0.lvn.1
- 0.2.4.
- Rebuild for VDR 1.3.31.

* Sun Aug 21 2005 Ville Skyttä <ville.skytta at iki.fi> - 0.2.3-1.lvn.4
- Rebuild for VDR 1.3.30.

* Fri Aug 19 2005 Dams <anvil[AT]livna.org> - 0.2.3-1.lvn.3
- Bumped release (rebuild against new ffmpeg)

* Tue Aug 16 2005 Ville Skyttä <ville.skytta at iki.fi> - 0.2.3-1.lvn.2
- Try to avoid build system problems by not using %%expand with vdr-config.

* Fri Aug 12 2005 Ville Skyttä <ville.skytta at iki.fi> - 0.2.3-1.lvn.1
- Convert docs to UTF-8.
- Improve description.
