%{!?scl:%global pkg_name %{name}}
%{?scl:%scl_package rubygem-%{gem_name}}
# Generated from introspection-0.0.2.gem by gem2rpm -*- rpm-spec -*-
%global gem_name introspection

Summary: Dynamic inspection of the hierarchy of method definitions on a Ruby object
Name: %{?scl_prefix}rubygem-%{gem_name}
Version: 0.0.3
Release: 2%{?dist}
Group: Development/Languages
# https://github.com/floehopper/introspection/issues/1
License: MIT
URL: http://jamesmead.org
Source0: http://rubygems.org/gems/%{gem_name}-%{version}.gem
# Remove instantiator dependency.
# https://github.com/floehopper/introspection/issues/2
Patch0: %{pkg_name}-%{version}-update-dep.patch
# Move to Minitest 5
# https://github.com/floehopper/introspection/pull/7
Patch1: rubygem-introspection-minitest5.patch
Requires: %{?scl_prefix_ruby}ruby(release)
Requires: %{?scl_prefix_ruby}ruby(rubygems)
Requires: %{?scl_prefix_ruby}ruby
Requires: %{?scl_prefix}rubygem(metaclass) => 0.0.1
Requires: %{?scl_prefix}rubygem(metaclass) < 0.1
# Seems to be useless ATM.
# https://github.com/floehopper/introspection/issues/2
# Requires: %{?scl_prefix}rubygem(instantiator) => 0.0.3
# Requires: %{?scl_prefix}rubygem(instantiator) < 0.1
BuildRequires: %{?scl_prefix_ruby}ruby(release)
BuildRequires: %{?scl_prefix_ruby}rubygems-devel
BuildRequires: %{?scl_prefix_ruby}ruby
BuildRequires: %{?scl_prefix}rubygem(metaclass) => 0.0.1
BuildRequires: %{?scl_prefix}rubygem(metaclass) < 0.1
# Required to satisfy the 'blankslate' require. May be replaced
# by rubygem(blankslate) when available in Fedora.
BuildRequires: %{?scl_prefix}rubygem(builder)
BuildRequires: %{?scl_prefix_ruby}rubygem(minitest)
BuildArch: noarch
Provides: %{?scl_prefix}rubygem(%{gem_name}) = %{version}

%description
Dynamic inspection of the hierarchy of method definitions on a Ruby object


%package doc
Summary: Documentation for %{pkg_name}
Group: Documentation
Requires: %{?scl_prefix}%{pkg_name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{pkg_name}


%prep
%setup -q -c -T
%{?scl:scl enable %{scl} - << \EOF}
%gem_install -n %{SOURCE0}
%{?scl:EOF}

pushd .%{gem_dir}
%patch0 -p1
popd

pushd .%{gem_instdir}
%patch1 -p1
popd

%build

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

%check
pushd .%{gem_instdir}
# Disable Bundler
sed -i '2,2d' test/test_helper.rb
%{?scl:scl enable %{scl} - << \EOF}
ruby -Ilib:test -e 'Dir.glob "./test/*_test.rb", &method(:require)'
%{?scl:EOF}
popd


%files
%dir %{gem_instdir}
%doc %{gem_instdir}/COPYING.txt
%exclude %{gem_instdir}/.gitignore
%exclude %{gem_instdir}/.travis.yml
%exclude %{gem_instdir}/introspection.gemspec
%{gem_libdir}
%{gem_instdir}/test
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_instdir}/README.md
%{gem_instdir}/Gemfile
%{gem_instdir}/Rakefile
%{gem_instdir}/samples
%doc %{gem_docdir}


%changelog
* Fri Jan 22 2016 Dominic Cleal <dcleal@redhat.com> 0.0.3-2
- Rebuild for sclo-ror42 SCL

* Mon Jan 19 2015 Josef Stribny <jstribny@redhat.com> - 0.0.3-1
- Update to 0.0.3

* Thu Jan 23 2014 Vít Ondruch <vondruch@redhat.com> - 0.0.2-9
- Remove version from RubyGems dependency.

* Tue Jun 04 2013 Josef Stribny <jstribny@redhat.com> - 0.0.2-8
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Wed Jul 25 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 0.0.2-7
- Specfile cleanup.

* Mon Apr 02 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 0.0.2-6
- Rebuilt for scl.

* Thu Jan 19 2012 Vít Ondruch <vondruch@redhat.com> - 0.0.2-5
- Rebuilt for Ruby 1.9.3.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Oct 04 2011 Vít Ondruch <vondruch@redhat.com> - 0.0.2-3
- Fix BuildRequires and test suite.
- Move README.md into -doc subpackage and mark it properly.

* Tue Oct 04 2011 Vít Ondruch <vondruch@redhat.com> - 0.0.2-2
- Clarified license.

* Mon Oct 03 2011 Vít Ondruch <vondruch@redhat.com> - 0.0.2-1
- Initial package
