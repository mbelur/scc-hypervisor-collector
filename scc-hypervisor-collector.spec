#
# spec file for package scc-hypervisor-collector
#
# Copyright (c) 2022 SUSE LLC
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via https://bugs.opensuse.org/
#


%define _not_yet 0
%define skip_python2 1
%global __python %{_bindir}/python3

%{?!python_module:%define python_module() python3-%{**}}
%{?!python_build:%define python_build %{expand:%py3_build}}
%{?!python_install:%define python_install %{expand:%py3_install}}

Name:           scc-hypervisor-collector
Version:        0.0.0~git0.a1b2c3d
Release:        0
Summary:        Collects/Uploads hypervisor details to SUSE Customer Care
License:        Apache-2.0
Group:          System/Management
URL:            https://github.com/SUSE/scc-hypervisor-collector
Source0:        scc-hypervisor-collector-%{version}.tar.xz
BuildRequires:  %{python_module PyYAML}
BuildRequires:  %{python_module devel}
BuildRequires:  fdupes
BuildRequires:  python-rpm-macros
BuildRequires:  %{python_module pytest}
BuildRequires:  %{python_module mock}
BuildRequires:  virtual-host-gatherer-Libvirt
BuildRequires:  virtual-host-gatherer-VMware
Requires:       %{python_module PyYAML}
Requires:       virtual-host-gatherer-Libvirt
Requires:       virtual-host-gatherer-VMware
BuildArch:      noarch
%if 0%{_not_yet}
BuildRequires:  asciidoc
%endif
%if 0%{?suse_version} < 1530
BuildRequires:  %{python_module setuptools}
%endif

%description
This package contains a script to gather information about virtual
machines running on various hypervisors & VM management solutions.

%prep
%setup -q -n scc-hypervisor-collector-%{version}

%build
%python_build

%install
%python_install

%if 0%{_not_yet}
a2x -v -d manpage -f manpage doc/%{name}.1.asciidoc
mkdir -p %{buildroot}%{_mandir}/man1
install -m 0644 doc/%{name}.1 %{buildroot}%{_mandir}/man1/
%endif

%fdupes %{buildroot}%{python_sitelib}

%check
export PYTHONPATH=%{buildroot}%{python_sitelib}

# ensure example config permissions are correct
chmod -R g-rwx,o-rwx examples
%{buildroot}%{_bindir}/%{name} -h
%{buildroot}%{_bindir}/%{name} --check --config examples/shc_cfg.yaml

# run tests
pytest -vv

%files
%{_bindir}/%{name}
%license LICENSE
%doc README.md
%if 0%{_not_yet}
%{_mandir}/man1/%{name}.1%{?ext_man}
%endif
%dir %{python_sitelib}/scc_hypervisor_collector
%{python_sitelib}/scc_hypervisor_collector/*.py*
%dir %{python_sitelib}/scc_hypervisor_collector/api
%{python_sitelib}/scc_hypervisor_collector/api/*.py*
%dir %{python_sitelib}/scc_hypervisor_collector/cli
%{python_sitelib}/scc_hypervisor_collector/cli/*.py*

%dir %{python_sitelib}/scc_hypervisor_collector/__pycache__
%{python_sitelib}/scc_hypervisor_collector/__pycache__/*.py*
%dir %{python_sitelib}/scc_hypervisor_collector/api/__pycache__
%{python_sitelib}/scc_hypervisor_collector/api/__pycache__/*.py*
%dir %{python_sitelib}/scc_hypervisor_collector/cli/__pycache__
%{python_sitelib}/scc_hypervisor_collector/cli/__pycache__/*.py*
%{python_sitelib}/scc_hypervisor_collector-*.egg-info

%changelog
