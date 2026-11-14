//! A tiny two-version target with hand-placed coverage points. It exists to test the Stage 2
//! pipeline end to end (base run, prior, trials, logs) before real targets are built. Do not
//! report results from it.
//!
//! Format: "FRED" then chunks of [4-byte tag][1-byte length][body].
//! v2 changes which mutations pay off: HEAD branches on low nibbles instead of high ones, BODY
//! checks 16-bit instead of 32-bit values, and a new META chunk appears.

pub const MAP_SIZE: usize = 1024;
pub static mut MAP: [u8; MAP_SIZE] = [0; MAP_SIZE];

fn hit(id: usize) {
    unsafe {
        let map = &raw mut MAP;
        (*map)[id % MAP_SIZE] = (*map)[id % MAP_SIZE].wrapping_add(1);
    }
}

pub fn run(data: &[u8], version: u8) {
    if data.len() < 4 || &data[..4] != b"FRED" {
        return;
    }
    hit(1);
    let mut rest = &data[4..];
    for depth in 0..8 {
        if rest.len() < 5 {
            return;
        }
        let end = (5 + rest[4] as usize).min(rest.len());
        let (tag, body) = (&rest[..4], &rest[5..end]);
        rest = &rest[end..];
        hit(10 + depth);
        match (tag, version) {
            (b"HEAD", 1) => body.iter().take(8).enumerate().for_each(|(i, b)| hit(100 + i * 16 + (b >> 4) as usize)),
            (b"HEAD", _) => body.iter().take(8).enumerate().for_each(|(i, b)| hit(100 + i * 16 + (b & 15) as usize)),
            (b"BODY", 1) if body.len() >= 4 => {
                let v = u32::from_le_bytes([body[0], body[1], body[2], body[3]]);
                hit(300 + v.leading_zeros() as usize);
                hit(340 + [0, 1, 0x7fff_ffff, 0x8000_0000, 0xffff_ffff].iter().position(|&x| x == v).unwrap_or(9));
            }
            (b"BODY", _) if body.len() >= 2 => {
                let v = u16::from_le_bytes([body[0], body[1]]);
                hit(300 + v.leading_zeros() as usize);
                hit(340 + [0, 1, 0x7fff, 0x8000, 0xffff].iter().position(|&x| x == v).unwrap_or(9));
            }
            (b"TAIL", _) => hit(400 + body.len()),
            (b"META", 2) => {
                hit(700);
                if body.starts_with(b"v2") {
                    body.iter().skip(2).take(16).for_each(|&b| hit(710 + (b % 32) as usize));
                }
            }
            _ => hit(9),
        }
    }
}
