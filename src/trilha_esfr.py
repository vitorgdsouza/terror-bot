"""Trilha própria do E Se Fosse Real?, sintetizada em código (sem bipes nem "sinais", sem direitos de terceiros).

Clima de documentário de ciência: acordes longos e quentes (pad), um arpejo suave tipo caixinha de música,
um baixo bem macio e reverb. Gera um loop de 64 s que emenda sem corte.
    python -m src.trilha_esfr saida.wav
"""
import sys
from pathlib import Path

import numpy as np

SR = 44100
BPM = 90
# progressão calma e "curiosa": Lá menor, Fá, Dó, Sol (com sétimas e nonas suaves)
ACORDES = [[57, 60, 64, 67, 71], [53, 57, 60, 64, 67], [48, 55, 60, 64, 67], [55, 59, 62, 66, 69]]


def _hz(m):
    return 440.0 * 2 ** ((m - 69) / 12)


def _pad(freq, dur, rnd):
    t = np.arange(int(dur * SR)) / SR
    s = np.zeros_like(t)
    for det in (-0.12, 0.0, 0.13):                       # três vozes levemente desafinadas = som largo
        f = freq * 2 ** (det / 12)
        fase = rnd.rand() * 6.28
        for h, a in ((1, 1.0), (2, 0.35), (3, 0.12), (4, 0.05)):
            s += a * np.sin(2 * np.pi * f * h * t + fase * h)
    env = np.minimum(1, t / 2.5) * np.minimum(1, (dur - t) / 2.5)   # entra e sai devagar
    trem = 1 + 0.08 * np.sin(2 * np.pi * 0.25 * t)
    return s * env * trem


def _nota(freq, dur):
    t = np.arange(int(dur * SR)) / SR
    s = np.sin(2 * np.pi * freq * t) + 0.25 * np.sin(2 * np.pi * freq * 2 * t) + 0.08 * np.sin(2 * np.pi * freq * 3 * t)
    return s * np.exp(-t * 3.2) * np.minimum(1, t / 0.005)


def _reverb(x, seg=2.8, mistura=0.35, rnd=None):
    n = int(seg * SR)
    ir = (rnd.randn(n) * np.exp(-np.arange(n) / SR * 3.0)).astype(np.float64)
    ir /= np.sqrt((ir ** 2).sum())
    tam = 1 << int(np.ceil(np.log2(len(x) + n)))
    y = np.fft.irfft(np.fft.rfft(x, tam) * np.fft.rfft(ir, tam), tam)[:len(x) + n]
    y[:n] += y[len(x):len(x) + n]                         # o rabo do reverb volta para o começo: o loop emenda
    y = y[:len(x)]
    return x * (1 - mistura) + y * mistura * 1.6


def gerar(destino: Path, seed: int = 7) -> Path:
    rnd = np.random.RandomState(seed)
    barra = 4 * 60 / BPM                                  # 1 compasso
    por_acorde = 4 * barra                                # 4 compassos por acorde
    total = por_acorde * len(ACORDES) * 2                 # 2 voltas na progressão (~85 s)
    n = int(total * SR)
    extra = int(6 * SR)                                   # o que passa do fim volta para o começo (loop sem emenda)
    pad, arp, baixo = np.zeros(n + extra), np.zeros(n + extra), np.zeros(n + extra)
    colcheia = 60 / BPM / 2
    padrao = [0, 2, 1, 3, 2, 4, 3, 1]                     # desenho do arpejo
    for volta in range(2):
        for k, ac in enumerate(ACORDES):
            ini = int((volta * len(ACORDES) + k) * por_acorde * SR)
            dur_pad = por_acorde + 2.5
            for m in ac[:4]:
                p = _pad(_hz(m), dur_pad, rnd)
                fim = min(n + extra, ini + len(p))
                pad[ini:fim] += p[:fim - ini] * 0.11
            b = _pad(_hz(ac[0] - 12), por_acorde + 1.0, rnd)
            fim = min(n + extra, ini + len(b))
            baixo[ini:fim] += b[:fim - ini] * 0.09
            if volta == 1 or k >= 2:                      # o arpejo entra depois, para o loop ter respiro
                for j in range(int(por_acorde / colcheia)):
                    if rnd.rand() < 0.18:                 # algumas notas faltam: soa humano, sem metrônomo
                        continue
                    m = ac[padrao[j % len(padrao)]] + 12
                    s = _nota(_hz(m), 1.6) * (0.07 + 0.03 * rnd.rand())
                    a = ini + int(j * colcheia * SR)
                    fim = min(n + extra, a + len(s))
                    arp[a:fim] += s[:fim - a]
    mix = pad + baixo + arp
    mix[:extra] += mix[n:]
    mix = mix[:n]
    # sobra do fim do loop volta ao começo (pads longos não cortam na emenda)
    mix = _reverb(mix, rnd=rnd)
    # passa-baixa suave: tira qualquer brilho agudo
    espectro = np.fft.rfft(mix)
    fr = np.fft.rfftfreq(len(mix), 1 / SR)
    espectro *= 1 / np.sqrt(1 + (fr / 3500) ** 4)
    mix = np.fft.irfft(espectro, len(mix))
    mix /= np.abs(mix).max() + 1e-9
    mix *= 0.8
    est = np.stack([mix, np.roll(mix, int(0.012 * SR))], -1)         # um pouco de largura estéreo
    import wave
    destino = Path(destino)
    destino.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(destino), "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((est * 32767).astype("<i2").tobytes())
    return destino


if __name__ == "__main__":
    print(gerar(Path(sys.argv[1] if len(sys.argv) > 1 else "trilha_esfr.wav")))
