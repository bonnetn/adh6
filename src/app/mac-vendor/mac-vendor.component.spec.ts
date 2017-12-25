import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { MacVendorComponent } from './mac-vendor.component';
import { HttpClientModule } from '@angular/common/http';

describe('MacVendorComponent', () => {
  let component: MacVendorComponent;
  let fixture: ComponentFixture<MacVendorComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ MacVendorComponent ],
      imports: [ HttpClientModule ],
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(MacVendorComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
