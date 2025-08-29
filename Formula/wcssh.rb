class Wcssh < Formula
  desc "A Warp-native multi-SSH launcher that opens a new window, splits panes, and enables synchronized input by default."
  homepage "https://github.com/waynelloyd/homebrew-wcssh"
  url "https://github.com/waynelloyd/homebrew-wcssh/archive/refs/tags/v1.0.2.tar.gz"
  sha256 "0ddf92f9670782f3dd3faf551d4addef2eb7c25ce60ba7466c32eb22ba65b8a2" # The checksum of the new v1.0.0 tarball
  license "MIT"

  def install
    bin.install "wcssh.py" => "wcssh"
  end

  test do
    system "#{bin}/wcssh", "--version"
  end
end
