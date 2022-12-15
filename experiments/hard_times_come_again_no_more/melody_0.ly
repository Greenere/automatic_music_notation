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
 \new Voice { \new Voice { \clef "treble" 
                \time 4/4
                r 8  
                c''' 4  
                fis' 4  
                g' 4  
                r 16  
                g'' 4  
                a'' 4  
                b'' 4  
                fis' 4  
                e'' 4  
                d'' 4  
                r 8  
                c''' 4  
                f' 4  
                r 16  
                a' 4  
                r 8  
                g' 4  
                fis'' 4  
                r 8  
                b'' 4  
                r 16  
                f'' 4  
                gis'' 4  
                r 16  
                fis' 4  
                e'' 4  
                fis' 4  
                r 4  
                r 4  
                r 4  
                r 4  
                r 8  
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
 
