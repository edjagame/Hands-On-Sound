const DEFAULT_VOLUME = 0.75

function clampVolume(volume: number): number {
  return Math.min(Math.max(volume, 0), 1)
}

export function getDefaultVolume(): number {
  return DEFAULT_VOLUME
}

export function getVolumeForHandPosition(
  normalizedY: number | undefined,
): number {
  if (normalizedY === undefined || !Number.isFinite(normalizedY)) {
    return DEFAULT_VOLUME
  }

  const legacyVolume = clampVolume(1 - normalizedY)

  return legacyVolume
}
