# takopi-demiurg

Run autonomous design sessions with demiurg.

## Usage

```
/demiurg <design-file>
```

Example:
```
/demiurg design.txt
```

Starts demiurg in background, monitors progress, reports completion or errors.

## How it works

Spawns `demiurg <design-file>` as a subprocess, waits for completion, returns status. The design file should be a path relative to the current working directory.

## Requirements

`demiurg` binary on PATH.

## Configuration

None.
