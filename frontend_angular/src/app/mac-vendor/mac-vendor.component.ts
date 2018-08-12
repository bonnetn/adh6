import {Component, Input, OnDestroy, OnInit} from '@angular/core';

import {HttpClient} from '@angular/common/http';

@Component({
  selector: 'app-mac-vendor',
  templateUrl: './mac-vendor.component.html',
  styleUrls: ['./mac-vendor.component.css']
})
export class MacVendorComponent implements OnInit, OnDestroy {

  @Input() mac: string;

  private alive = true;

  constructor(
    private http: HttpClient,
  ) {
  }

  ngOnInit() {
    /*this.http.get( "https://api.macvendors.com/" + this.mac, {
      responseType: "text"
    })
      .takeWhile( () => this.alive )
      .subscribe(( data:string) => {
        this.vendor = data;
      },
        ( err : HttpErrorResponse) => {
          this.vendor = "Unknown";
        });*/
  }

  ngOnDestroy() {
    this.alive = false;
  }

}
