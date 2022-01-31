import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RankingTypeComponent } from './ranking-type.component';

describe('RankingTypeComponent', () => {
  let component: RankingTypeComponent;
  let fixture: ComponentFixture<RankingTypeComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ RankingTypeComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(RankingTypeComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
