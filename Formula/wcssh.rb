class Wcssh < Formula
  desc "A Warp-native multi-SSH launcher that opens a new window, splits panes, and enables synchronized input by default."
  homepage "https://github.com/waynelloyd/homebrew-wcssh"
  url "https://github.com/waynelloyd/homebrew-wcssh/archive/refs/tags/v1.0.2.tar.gz"
  sha256 "7c3fa396a87dea32a18cc5386310155d52beac342a55f370b2c9b762e21eecef" # The checksum of the new v1.0.0 tarball
  license "MIT"

  def install
    bin.install "wcssh.py" => "wcssh"
  end

  test do
    system "#{bin}/wcssh", "--version"
  end
end
