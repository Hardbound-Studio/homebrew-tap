cask "sortbook" do
  version "1.0.7"
  sha256 "fedd43141bdb8b8ea05784102af59bdca7eb1fcb42b9375e5fb69a4e0956cd2e"

  url "https://sortbook.app/download/Sortbook_#{version}_aarch64.dmg"
  name "Sortbook"
  desc "Move the files in your folders into subfolders by type, month or year"
  homepage "https://sortbook.app/"

  livecheck do
    url "https://sortbook.app/download/"
    regex(/Sortbook[._-]v?(\d+(?:\.\d+)+)[._-]aarch64\.dmg/i)
  end

  auto_updates true
  depends_on arch: :arm64
  depends_on macos: :monterey

  app "Sortbook.app"

  zap trash: [
    "~/Library/Application Support/com.hardboundstudio.sortbook",
    "~/Library/Caches/com.hardboundstudio.sortbook",
    "~/Library/Preferences/com.hardboundstudio.sortbook.plist",
    "~/Library/WebKit/com.hardboundstudio.sortbook",
  ]
end
