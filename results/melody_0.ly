\version "2.22" 
\include "lilypond-book-preamble.ly"
    
color = #(define-music-function (parser location color) (string?) #{
        \once \override NoteHead #'color = #(x11-color color)
        \once \override Stem #'color = #(x11-color color)
        \once \override Rest #'color = #(x11-color color)
        \once \override Beam #'color = #(x11-color color)
     #})
    
\header { } 
\score  { 
 \new Voice { \new Voice { \clef "alto" 
                \time 4/4
                e' 4  
                ais 4  
                b 4  
                cis' 4  
                dis' 4  
                f' 4  
                fis' 4  
                d' 4  
                cis' 4  
                b 4  
                ais 4  
                dis' 4  
                f' 4  
                b' 4  
                r 16  
                ais 4  
                c' 4  
                d' 4  
                dis' 4  
                fis' 4  
                f' 4  
                d' 4  
                cis' 4  
                b 4  
                ais 4  
                r 16  
                f' 2  
                r 16  
                 } 
               
 
           } 
         
 
  } 
 
\paper { }
\layout {
  \context {
    \RemoveEmptyStaffContext
    \override VerticalAxisGroup #'remove-first = ##t
  }
 }
 
