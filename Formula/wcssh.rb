class Wcssh < Formula
  desc "A Warp-native multi-SSH launcher that opens a new window, splits panes, and enables synchronized input by default."
  homepage "https://github.com/waynelloyd/homebrew-wcssh"
  url "https://github.com/waynelloyd/homebrew-wcssh/archive/refs/tags/v1.0.1.tar.gz"
  sha256 "48382794a9b061e73267f7b093c2569f16893f939d481f5470a036285cab2859" # The checksum of the new v1.0.0 tarball
  license "MIT"

  def install
    bin.install "wcssh.py" => "wcssh"
  end

  test do
    system "#{bin}/wcssh", "--version"
  end
end
