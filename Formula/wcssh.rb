class Wcssh < Formula
  desc "A Warp-native multi-SSH launcher that opens a new window, splits panes, and enables synchronized input by default."
  homepage "https://github.com/waynelloyd/homebrew-wcssh"
  url "https://github.com/waynelloyd/homebrew-wcssh/archive/refs/tags/v1.0.2.tar.gz"
  sha256 "6642ff0d50cd2fdd5a36c8bb362551618a729e6564d85125728af8204b0732bc" # To get this, create a release and run: shasum -a 256 v1.0.3.tar.gz
  license "MIT"

  def install
    bin.install "wcssh.py" => "wcssh"
  end

  test do
    system "#{bin}/wcssh", "--version"
  end
end
