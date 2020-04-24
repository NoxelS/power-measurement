type VPTFile = string;

interface VPTData {
  extractDataOutOfVPTFile: (VPTFile) => void;
}

export class VPT implements VPTData {
  private _metaData;

  data: number[][];
  labels: string[];
  min: number;
  max: number;

  constructor(vptFile: VPTFile) {
    this.extractDataOutOfVPTFile(vptFile);
  }

  extractDataOutOfVPTFile(file: VPTFile) {
    // TODO: Improve regex
    const lines = file.split(/\r\n/g);
    const [metaDataString] = lines.splice(0, 1);
    this._metaData = {
      dateOfMeasurement: metaDataString.split('-')[0],
    };
  }
}
