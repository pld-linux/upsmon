Summary:	Allows to monitor UPS from Fideltronik
Summary(pl):	Zapewnia monitoring UPSów firmy Fideltronik
Name:		upsmon
Version:	2.2
Release:	0.1
Epoch:		1
License:	Free
Group:		Daemons
Source0:	http://www.fideltronik.com.pl/pl_products/upsmon/software/2x_linux/%{name}22s.tar
Source1:	%{name}.init
Patch0:		upsmon-acfail.patch
Patch1:		upsmon-conf.patch
Patch2:		upsmon-message.patch
URL:		http://www.fideltronik.com.pl/
ExclusiveArch:	%{ix86}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/ups

%description
Allows to monitor UPS from Fideltronik.

%description -l pl
Zapewnia monitoring i bezpieczne zamkniêcie systemu operacyjnego
komputera z do³±czonym zasilaczem UPS, oraz powiadamianie stacji
roboczych z zainstalowanym UPS Monitor Client.

%prep
%setup -q -c %{name}-%{version}
%patch0
%patch1
%patch2

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},/sbin,%{_sysconfdir}/scripts,/etc/rc.d/init.d,/var/log}

install server/scripts/* $RPM_BUILD_ROOT%{_sysconfdir}/scripts/
install server/*.conf $RPM_BUILD_ROOT%{_sysconfdir}/
install server/upsd $RPM_BUILD_ROOT%{_sbindir}/fidel-upsd
install server/upsoff $RPM_BUILD_ROOT/sbin/
install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/upsd
install server/upsd.log $RPM_BUILD_ROOT/var/log/upsd.log

ln -sf /var/log/upsd.log $RPM_BUILD_ROOT%{_sysconfdir}/upsd.log 

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add upsd
if [ -f /var/lock/subsys/upsd ]; then
        /etc/rc.d/init.d/upsd restart 1>&2
else
        echo "Run \"/etc/rc.d/init.d/upsd start\" to start upsd daemon."
fi

%preun
if [ "$1" = "0" ]; then
        if [ -f /var/lock/subsys/upsd ]; then
                /etc/rc.d/init.d/upsd stop 1>&2
        fi
        /sbin/chkconfig --del upsd
fi

%files
%defattr(644,root,root,755)
%doc czytaj.to
%attr(750,root,root) %{_sbindir}/*
%attr(750,root,root) /sbin/*
%attr(750,root,root) %dir %{_sysconfdir}
%attr(750,root,root) %dir %{_sysconfdir}/scripts
%attr(755,root,root) %config(noreplace) %{_sysconfdir}/scripts/*.sh
%attr(644,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/*.conf
%ghost %attr(644,root,root) %{_sysconfdir}/upsd.log
%attr(755,root,root) /etc/rc.d/init.d/upsd
%attr(644,root,root) /var/log/upsd.log
