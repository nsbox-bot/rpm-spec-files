%global goipath github.com/refi64/nsbox

%define reldir() %{lua:\
  local arg = rpm.expand('%1')\
  local prefix = rpm.expand('%{_prefix}')\
  assert(arg:sub(1, prefix:len()) == prefix, "arg " .. arg .. " does not start with " .. prefix)\
  local result = arg:sub(prefix:len() + 1):gsub('^/', '')\
  print(result)}

%global relbindir %{reldir %{_bindir}}
%global rellibexecdir %{reldir %{_libexecdir}}
%global reldatadir %{reldir %{_datadir}}

# nsbox-host has missing build-ids due to being static.
%global _missing_build_ids_terminate_build 0
# Scripts in data/scripts intentionally use a hashbang of /bin/bash (not /usr/bin)
# because the scripts are run inside container OSs that may not have performed the /usr
# merge yet. Skip automatically converting those hashbangs to /usr/bin/bash.
%global __brp_mangle_shebangs_exclude .*\.sh

Name: nsbox-edge
Version: 20.03.22.230
%if "%{name}" == "nsbox-edge"
Release: 1%{?dist}.99e2673
%else
Release: 1%{?dist}
%endif
Summary: A multi-purpose, nspawn-powered container manager
License: MPL-2.0
URL: https://nsbox.dev/
BuildRequires: gcc
BuildRequires: gn
BuildRequires: go-rpm-macros
BuildRequires: golang
BuildRequires: ninja-build
BuildRequires: python3
BuildRequires: selinux-policy-devel
BuildRequires: systemd-devel
Requires: container-selinux
Requires: %{name}-selinux == %{version}-%{release}
Requires: polkit
Requires: sudo
Requires: systemd-container
Source0: nsbox-sources.tar
BuildRequires: golang(github.com/briandowns/spinner)
BuildRequires: golang(github.com/coreos/go-systemd/daemon)
BuildRequires: golang(github.com/coreos/go-systemd/dbus)
BuildRequires: golang(github.com/coreos/go-systemd/journal)
BuildRequires: golang(github.com/coreos/go-systemd/machine1)
BuildRequires: golang(github.com/coreos/go-systemd/sdjournal)
BuildRequires: golang(github.com/coreos/go-systemd/util)
BuildRequires: golang(github.com/coreos/pkg/dlopen)
BuildRequires: golang(github.com/dustin/go-humanize)
BuildRequires: golang(github.com/godbus/dbus)
BuildRequires: golang(github.com/google/go-cmp/cmp/internal/diff)
BuildRequires: golang(github.com/google/go-cmp/cmp/internal/flags)
BuildRequires: golang(github.com/google/go-cmp/cmp/internal/function)
BuildRequires: golang(github.com/google/go-cmp/cmp/internal/value)
BuildRequires: golang(github.com/google/go-cmp/cmp)
BuildRequires: golang(github.com/google/go-cmp/cmp/cmpopts)
BuildRequires: golang(github.com/google/go-cmp/cmp/internal/testprotos)
BuildRequires: golang(github.com/google/go-cmp/cmp/internal/teststructs)
BuildRequires: golang(github.com/google/subcommands)
BuildRequires: golang(github.com/kr/pty)
BuildRequires: golang(github.com/opencontainers/selinux/go-selinux)
BuildRequires: golang(github.com/pkg/errors)
BuildRequires: golang(github.com/vishvananda/netlink/nl)
BuildRequires: golang(github.com/vishvananda/netlink)
BuildRequires: golang(golang.org/x/crypto/ssh/terminal)
BuildRequires: golang(golang.org/x/sync/errgroup)
BuildRequires: golang(golang.org/x/sys/unix)
BuildRequires: golang(k8s.io/apimachinery/pkg/util/runtime)
BuildRequires: golang(k8s.io/apimachinery/pkg/util/wait)
%define setup_go_repo_links \
cd %{_builddir}/%{name}-%{version}\
mkdir -p vendor/github.com/briandowns\
ln -sf %{gopath}/src/github.com/briandowns/spinner vendor/github.com/briandowns/spinner\
mkdir -p vendor/github.com/coreos\
ln -sf %{gopath}/src/github.com/coreos/go-systemd vendor/github.com/coreos/go-systemd\
mkdir -p vendor/github.com/coreos\
ln -sf %{gopath}/src/github.com/coreos/pkg vendor/github.com/coreos/pkg\
mkdir -p vendor/github.com/dustin\
ln -sf %{gopath}/src/github.com/dustin/go-humanize vendor/github.com/dustin/go-humanize\
mkdir -p vendor/github.com/fatih\
ln -sf %{gopath}/src/github.com/fatih/color vendor/github.com/fatih/color\
mkdir -p vendor/github.com/godbus\
ln -sf %{gopath}/src/github.com/godbus/dbus vendor/github.com/godbus/dbus\
mkdir -p vendor/github.com/google\
ln -sf %{gopath}/src/github.com/google/go-cmp vendor/github.com/google/go-cmp\
mkdir -p vendor/github.com/google\
ln -sf %{gopath}/src/github.com/google/subcommands vendor/github.com/google/subcommands\
mkdir -p vendor/github.com/kr\
ln -sf %{gopath}/src/github.com/kr/pty vendor/github.com/kr/pty\
mkdir -p vendor/github.com/mattn\
ln -sf %{gopath}/src/github.com/mattn/go-colorable vendor/github.com/mattn/go-colorable\
mkdir -p vendor/github.com/mattn\
ln -sf %{gopath}/src/github.com/mattn/go-isatty vendor/github.com/mattn/go-isatty\
mkdir -p vendor/github.com/opencontainers\
ln -sf %{gopath}/src/github.com/opencontainers/selinux vendor/github.com/opencontainers/selinux\
mkdir -p vendor/github.com/pkg\
ln -sf %{gopath}/src/github.com/pkg/errors vendor/github.com/pkg/errors\
mkdir -p vendor/github.com/vishvananda\
ln -sf %{gopath}/src/github.com/vishvananda/netlink vendor/github.com/vishvananda/netlink\
mkdir -p vendor/github.com/vishvananda\
ln -sf %{gopath}/src/github.com/vishvananda/netns vendor/github.com/vishvananda/netns\
mkdir -p vendor/golang.org/x\
ln -sf %{gopath}/src/golang.org/x/crypto vendor/golang.org/x/crypto\
mkdir -p vendor/golang.org/x\
ln -sf %{gopath}/src/golang.org/x/sync vendor/golang.org/x/sync\
mkdir -p vendor/golang.org/x\
ln -sf %{gopath}/src/golang.org/x/sys vendor/golang.org/x/sys\
mkdir -p vendor/k8s.io\
ln -sf %{gopath}/src/k8s.io/apimachinery vendor/k8s.io/apimachinery\
mkdir -p vendor/k8s.io\
ln -sf %{gopath}/src/k8s.io/klog vendor/k8s.io/klog\
:
Source2: https://github.com/GehirnInc/crypt/archive/6c0105aabd46.tar.gz#/github-com-GehirnInc-crypt-6c0105aabd46.tar.gz
Source3: https://github.com/artyom/untar/archive/v1.0.0.tar.gz#/github-com-artyom-untar-v1.0.0.tar.gz
Source4: https://github.com/google/go-containerregistry/archive/31e00cede111.tar.gz#/github-com-google-go-containerregistry-31e00cede111.tar.gz
Source5: https://github.com/refi64/go-lxtempdir/archive/e8f0a4e7825f.tar.gz#/github-com-refi64-go-lxtempdir-e8f0a4e7825f.tar.gz
Source6: https://github.com/varlink/go/archive/b83e34ab175f.tar.gz#/github-com-varlink-go-b83e34ab175f.tar.gz
%define setup_go_archives_universal \
%setup -q -T -c -n %{name}-%{version}/vendor/github.com/GehirnInc/crypt\
tar --strip-components=1 -xf %{S:2}\
%setup -q -T -c -n %{name}-%{version}/vendor/github.com/artyom/untar\
tar --strip-components=1 -xf %{S:3}\
%setup -q -T -c -n %{name}-%{version}/vendor/github.com/google/go-containerregistry\
tar --strip-components=1 -xf %{S:4}\
%setup -q -T -c -n %{name}-%{version}/vendor/github.com/refi64/go-lxtempdir\
tar --strip-components=1 -xf %{S:5}\
%setup -q -T -c -n %{name}-%{version}/vendor/github.com/varlink/go\
tar --strip-components=1 -xf %{S:6}\
:


%description
nsbox is a multi-purpose, nspawn-powered container manager.

%package selinux
BuildArch: noarch
Summary: SELinux policy for %{name}
%{?selinux_requires}
%description selinux
This is the SELinux policy for %{name}.

%package bender
Summary: Build images for nsbox
Requires: ansible-bender
Requires: podman
Requires: python3
%description bender
nsbox-bender is a script built on top of ansible-bender to build base images for your nsbox
containers.

%if "%{name}" == "nsbox-edge"

%package alias
Summary: Alias for nsbox-edge
%description alias
Installs the nsbox alias for nsbox-edge.

%package bender-alias
Summary: Alias for nsbox-edge-bender
%description bender-alias
Installs the nsbox-bender alias for nsbox-edge-bender.

%endif

%prep
rm -rf %{name}-%{version}

# Order of these commands is important!
%setup_go_archives_universal

%setup -q -D

%setup_go_repo_links

# @ is here for substitute_file.py.
cat >build/go-shim.sh <<'EOF'
#!/bin/sh
if [[ "$1" == "build" ]]; then
  shift
  %gobuild "$@"
else
  go "$@"
fi
EOF

sed -i 's/GO111MODULE=off//g' build/go-shim.sh
chmod +x build/go-shim.sh

%build
%set_build_flags
unset LDFLAGS

mkdir -p out
cat >out/args.gn <<EOF
go_exe = "$PWD/build/go-shim.sh"
prefix = "%{_prefix}"
bin_dir = "%{relbindir}"
libexec_dir = "%{rellibexecdir}"
share_dir = "%{reldatadir}"
state_dir = "%{_sharedstatedir}"
config_dir = "%{_sysconfdir}"
enable_selinux = true
override_release_version = "20.03.22.230"
%if "%{name}" != "nsbox-edge"
is_stable_build = true
%endif
EOF

gn gen out
ninja -C out

%install
mkdir -p %{buildroot}/%{_prefix}
cp -r out/install/%{_sysconfdir} %{buildroot}
cp -r out/install/{%{relbindir},%{rellibexecdir},%{reldatadir}} %{buildroot}/%{_prefix}
chmod -R g-w %{buildroot}

%pre selinux
%selinux_relabel_pre

%post selinux
%selinux_modules_install %{_datadir}/selinux/packages/%{name}.pp.bz2

%postun selinux
if [ $1 -eq 0 ]; then
  %selinux_modules_uninstall %{name}
fi

%posttrans selinux
%selinux_relabel_post

%files
%{_bindir}/%{name}
%{_sysconfdir}/profile.d/%{name}.sh
%{_libexecdir}/%{name}/nsboxd
%{_libexecdir}/%{name}/nsbox-invoker
%{_libexecdir}/%{name}/nsbox-host
%{_datadir}/%{name}/data/getty-override.conf
%{_datadir}/%{name}/data/wants-networkd.conf
%{_datadir}/%{name}/data/nsbox-container.target
%{_datadir}/%{name}/data/nsbox-init.service
%{_datadir}/%{name}/data/scripts/nsbox-apply-env.sh
%{_datadir}/%{name}/data/scripts/nsbox-enter-run.sh
%{_datadir}/%{name}/data/scripts/nsbox-enter-setup.sh
%{_datadir}/%{name}/data/scripts/nsbox-init.sh
%{_datadir}/%{name}/images/arch/Dockerfile
%{_datadir}/%{name}/images/arch/metadata.json
%{_datadir}/%{name}/images/arch/playbook.yaml
%{_datadir}/%{name}/images/arch/roles/main/tasks/main.yaml
%{_datadir}/%{name}/images/debian/Dockerfile
%{_datadir}/%{name}/images/debian/metadata.json
%{_datadir}/%{name}/images/debian/playbook.yaml
%{_datadir}/%{name}/images/debian/roles/main/tasks/main.yaml
%{_datadir}/%{name}/images/fedora/metadata.json
%{_datadir}/%{name}/images/fedora/playbook.yaml
%{_datadir}/%{name}/images/fedora/roles/main/tasks/main.yaml
%{_datadir}/%{name}/images/fedora/roles/main/templates/nsbox.repo
%{_datadir}/%{name}/release/VERSION
%{_datadir}/%{name}/release/BRANCH
%{_datadir}/polkit-1/actions/dev.nsbox.edge.policy
%{_datadir}/polkit-1/rules.d/dev.nsbox.edge.rules

%files selinux
%{_datadir}/selinux/packages/%{name}.pp.bz2

%files bender
%{_bindir}/%{name}-bender
%{_datadir}/%{name}/python/%{name}-bender.py*

%if "%{name}" == "nsbox-edge"

%files alias
%{_bindir}/nsbox

%files bender-alias
%{_bindir}/nsbox-bender

%endif
