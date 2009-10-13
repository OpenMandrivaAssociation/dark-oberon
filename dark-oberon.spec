%define	name	dark-oberon
%define	version	1.0.2
%define	pre	RC2
%define	release	0.rc2.3
%define	Summary	Dark Oberon

Name:		%{name}
Version:	%{version}
Release:	%mkrel %{release}
Group:		Games/Strategy
Source0:	%{name}-%{version}-%{pre}.tar.lzma
Source11:	%{name}-16x16.png
Source12:	%{name}-32x32.png
Source13:	%{name}-48x48.png
#Patch0:		dark-oberon-1.0.2-RC1-mdkconf.patch.bz2
Patch1:		dark-oberon-1.0.2-rc2-compile-fixes.patch	
Patch2:		fix_format_build.patch
Patch3:		fix_makefile_xrandr_lib_missing.patch
Url:		http://dark-oberon.sourceforge.net/
Summary:	%{Summary}
License:	GPLv2 BY-NC-SA BY-NC-ND
BuildRequires:	X11-devel glfw Mesa-common-devel lzma
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

ExclusiveArch:  %{ix86}

%description
Dark Oberon is an open source real-time strategy game similar to Warcraft II
released under GPL. It has got awesome graphics - textures created from
shots of real models made out of plasticine!

%prep
%setup -q -n %{name}-%{version}-%{pre}
#%patch0 -p1 -b .mdkconf
%patch1 -p0  -b .fixes
%patch2 -p1
%patch3 -p1

find -name CVS|xargs rm -rf
cd src
sh create_makefile.sh

%build
%make DEFINES="-DDATA_DIR='\"%{_gamesdatadir}/%{name}/\"' -DUNIX=1 -DSOUND=0 -DDEBUG=0" CPPFLAGS="%{optflags}"

%install
rm -rf %{buildroot}
install -m755 dark-oberon -D %{buildroot}%{_gamesbindir}/%{name}
install -d %{buildroot}%{_gamesdatadir}/%{name}
cp -r dat maps races schemes -d %{buildroot}%{_gamesdatadir}/%{name}

mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=Dark Oberon
Comment=%{Summary}
Exec=%{_gamesbindir}/%{name}
Icon=%{name}
Terminal=false
Type=Application
StartupNotify=true
Categories=Game;StrategyGame;
EOF

install -m644 %{SOURCE11} -D %{buildroot}%{_miconsdir}/%{name}.png
install -m644 %{SOURCE12} -D %{buildroot}%{_iconsdir}/%{name}.png
install -m644 %{SOURCE13} -D %{buildroot}%{_liconsdir}/%{name}.png

%if %mdkversion < 200900
%post
%update_menus
%endif

%if %mdkversion < 200900
%postun
%clean_menus
%endif

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc README docs/*
%{_gamesbindir}/*
%{_gamesdatadir}/%{name}
%{_datadir}/applications/mandriva-%{name}.desktop
%{_miconsdir}/%{name}.png
%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
