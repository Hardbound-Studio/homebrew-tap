cask "leaserail" do
  version "0.2.0"
  sha256 "746a8bb0b3fa0a476ca5c7df17592c4b5a1c17111963d5812edd5d421864ab6a"

  url "https://downloads.leaserail.app/LeaseRail-#{version}-mac.zip"
  name "LeaseRail"
  desc "Turn a folder of tenancy contracts into clean data"
  homepage "https://leaserail.app/"

  livecheck do
    url "https://leaserail.app/download/"
    regex(/LeaseRail[._-]v?(\d+(?:\.\d+)+)[._-]mac\.zip/i)
  end

  depends_on arch: :arm64
  depends_on macos: :sonoma

  app "LeaseRail.app"
end
