import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class DataService {
  private _headers: string[];
  private _columns: any[][];
  private _indieces: { [key: string]: number } = {};
  private _sampleCount: number;
  private _probabilities: number[] = [];

  private _unlabeledSamples = new Set<string>();

  private _estimationIndicies = [3, 4, 5];
  private _labelIndicies = [6, 7, 8];
  private _keyIndex = 1;

  constructor() {

  }

  public loadDataset(dataset: string) {
    const sep = '\t';
    const lines = dataset.split('\r\n');
    this._headers = lines[0].split(sep);

    this._columns = [...Array(this._headers.length).keys()].map(() => []);

    for (let r = 1; r < lines.length; r++) {
      const values = lines[r].split(sep);
      const key = values[this._keyIndex];

      if (this._labelIndicies.map(index => values[index]).every(v => v == '')) {
        this._unlabeledSamples.add(key);
      }

      this._indieces[key] = r - 1;
      let maxProbabity = 0;
      for (let c = 0; c < values.length; c++) {
        this._columns[c].push(values[c]);
        if (this._estimationIndicies.includes(c)) {
          const val = Number.parseFloat(values[c]);
          if (val > maxProbabity) maxProbabity = val;
        }
      }

      this._probabilities[r-1] = maxProbabity;
    }

    this._sampleCount = lines.length - 1;
  }

  public getFilepath(key: string) {
    const row = this._indieces[key];
    return this._columns[0][row] + '/' + this._columns[1][row];
  }

  public getNextSample(): string {
    // uncertainty sampling
    let bestKey: string;
    let bestValue = Number.POSITIVE_INFINITY;

    for (const key of this._unlabeledSamples) {
      let value = this._probabilities[this._indieces[key]];

      if (value < bestValue) {
        bestValue = value;
        bestKey = key;
      }
    }

    return bestKey;
  }

  public setLabel(key: string, labelIndex: number) {
    const row = this._indieces[key];
    for (let i = 0; i < this._labelIndicies.length; i++) {
      this._columns[this._labelIndicies[i]][row] = (i === labelIndex) ? '1' : '0';
    }

    this._unlabeledSamples.delete(key);
  }

  public getEstimations(key): number[] {
    const row = this._indieces[key];
    return this._estimationIndicies.map(index => this._columns[index][row]);
  }

  public downloadDataset() {
    const sep = '\t';
    let output = this._headers.join(sep);

    for (let row = 0; row < this._sampleCount; row++) {
      output += '\r\n' + this._columns.map(col => col[row]).join(sep);
    }
    const blob = new Blob([output], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    window.open(url);
  }
}
