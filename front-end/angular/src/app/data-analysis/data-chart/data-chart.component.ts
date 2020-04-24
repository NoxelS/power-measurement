import { Component, OnInit, Input, AfterContentInit, OnChanges } from '@angular/core';
import { ChartDataSets, ChartOptions, ChartType } from 'chart.js';
import { Color, Label } from 'ng2-charts';

@Component({
  selector: 'app-data-chart',
  templateUrl: './data-chart.component.html',
  styleUrls: ['./data-chart.component.scss'],
})
export class DataChartComponent implements OnInit, OnChanges {
  @Input() data: {
    voltage: number;
    power: number;
    time: string;
    channel: string;
  }[];

  @Input() labels: string[];

  public lineChartData: ChartDataSets[] = [];
  public lineChartLabels: Label[] = [];
  public lineChartOptions: ChartOptions = {
    responsive: true,
  };
  public lineChartColors: Color[] = [
    {
      borderColor: '#673ab7',
      backgroundColor: 'rgba(255,255,255,0)',
    },
  ];
  public lineChartLegend = false;
  public lineChartType: ChartType = 'line';
  public lineChartPlugins = [];

  constructor() {}

  ngOnInit() {}

  ngOnChanges() {
    this.lineChartData.push({ data: this.data.map((data) => data.voltage), label: this.data[0].channel });
    this.lineChartLabels = this.labels;
  }
}
