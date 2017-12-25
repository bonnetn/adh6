import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { RoomDetailsComponent } from './room-details.component';

import { RouterTestingModule } from '@angular/router/testing';
import { ApiModule } from '../api/api.module';

describe('RoomDetailsComponent', () => {
  let component: RoomDetailsComponent;
  let fixture: ComponentFixture<RoomDetailsComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ RoomDetailsComponent ]
      imports: [
        ApiModule,
        RouterTestingModule,
      ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(RoomDetailsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
