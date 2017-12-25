import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { MemberDetailsComponent } from './member-details.component';
import { RouterTestingModule } from '@angular/router/testing';
import { MacVendorComponent } from '../mac-vendor/mac-vendor.component';
import { ReactiveFormsModule } from '@angular/forms';
import { ApiModule } from '../api/api.module';

describe('MemberDetailsComponent', () => {
  let component: MemberDetailsComponent;
  let fixture: ComponentFixture<MemberDetailsComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ 
        MemberDetailsComponent,
        MacVendorComponent,
      ],
      imports: [ 
        RouterTestingModule,
        ReactiveFormsModule,
        ApiModule,
      ],
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(MemberDetailsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
