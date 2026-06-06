cask "audx" do
  version "0.1.2"
  sha256 "bcd8a8e6384f0baef5ae8c33b2b752df0cf3abcd1e9f7ebec9573dcf5cef8af2"

  url "https://github.com/kwong/audx/releases/download/v#{version}/audx-#{version}.dmg"
  name "audx"
  desc "Menu bar utility for switching audio input and output devices"
  homepage "https://github.com/kwong/audx"

  livecheck do
    url :url
    strategy :github_latest
  end

  app "audx.app"

  zap trash: [
    "~/Library/Application Support/audx",
    "~/Library/Caches/com.wkngw.audx",
    "~/Library/HTTPStorages/com.wkngw.audx",
    "~/Library/Preferences/com.wkngw.audx.plist",
    "~/Library/Saved Application State/com.wkngw.audx.savedState",
  ]
end
